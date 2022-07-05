"""
imports for functionality
"""
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe

from checkout.wh_handler import StripeWHHandler

# https://stripe.com/docs/webhooks


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get webhook data
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # webhook handler
    handler = StripeWHHandler(request)

    # map webhook events
    event_map = {
        'payment_intent.succeeded': handler.handle_successful_payment_intent,
        'payment_intent.payment_failed': handler.handle_failed_payment_intent,
    }

    # get type from stripe
    event_type = event['type']

    # if handler in event map, use that otherwise use default from stripe
    event_handler = event_map.get(event_type, handler.handle_event)

    # call event handler
    response = event_handler(event)
    return response
