/*
    https://stripe.com/docs/payments/accept-a-payment
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#stripe_public_key_id').text().slice(1, -1);
var stripe_secret_key = $('#stripe_secret_key_id').text().slice(1, -1);
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
    }
};

card.mount('#card-element');