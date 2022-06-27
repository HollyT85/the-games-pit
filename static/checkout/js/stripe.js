/*
    https://stripe.com/docs/payments/accept-a-payment
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#stripe_public_key_id').text().slice(1, -1);
var client_secret = $('#client_secret_id').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
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

