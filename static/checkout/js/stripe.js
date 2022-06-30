/*
    https://stripe.com/docs/payments/accept-a-payment
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#stripe_public_key_id').text().slice(1, -1);
var clientSecret = $('#client_secret_id').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card', {style: style});
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    },
};

card.mount('#card-element');

// errors 

card.addEventListener('change', function (event) {
    var cardErrors = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span role="alert">
                <i class="fas fa-bug"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(cardErrors).html(html);
    } else {
        cardErrors.textContent = '';
    }
});

// Form submit
var form = document.getElementById('payment');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // get info for save order
    var saveOrder = Boolean($('#save-info').attr('checked'))
    // use csrf token
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_order': saveOrder,
    };
    var url = '/checkout/cache_checkout_info/';

    $.post(url, postData).done(function(){
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.address_line1.value),
                        line2: $.trim(form.address_line2.value),
                        state: $.trim(form.county.value),
                        city: $.trim(form.town_city.value),
                        country: $.trim(form.country.value)
                    }
                },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone.value),
                address:{
                    line1: $.trim(form.address_line1.value),
                    line2: $.trim(form.address_line2.value),
                    city: $.trim(form.town_city.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.post_code.value),
                    country: $.trim(form.country.value)
                    }
                }
            }
        }).then(function(result) {
            if (result.error) {
                var cardErrors = document.getElementById('card-errors');
                var html = `
                    <span role="alert">
                        <i class="fas fa-bug"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(cardErrors).html(html);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function(){
        // reload page if fails
        location.reload();
    });
});
