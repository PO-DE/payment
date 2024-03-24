# from typing import Any
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import send_mail
# from django.shortcuts import redirect
# from django.views.generic import TemplateView
# from django.views import View
# from .models import Product
# import stripe
# from django.conf import settings
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
# class SuccessView(TemplateView):
#     template_name = "Success.html"
#
# class CancelView(TemplateView):
#     template_name = "Cancel.html"
#
# class ProductLandingPageView(TemplateView):
#     template_name = 'landing.html'
#
#     def get_context_data(self, **kwargs: Any):
#         product = Product.objects.get(name="Test Product")
#         context = super().get_context_data(**kwargs)
#         context.update({
#             "product": product,
#             "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
#         })
#         return context
#
# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = self.kwargs.get("pk")
#         product = Product.objects.get(id=product_id)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': product.price,
#                         'product_data': {
#                             'name': product.name,
#                             'images': [product.url],
#                         },
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url=YOUR_DOMAIN + '/success/',
#                 cancel_url=YOUR_DOMAIN + '/cancel/',
#                 metadata={
#                     'product_id': str(product.id)
#                 }
#             )
#             return redirect(checkout_session.url)
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
#
#
# @csrf_exempt
# def my_stripe_webhook_view(request):
#     if request.method == 'POST':
#         payload = request.body
#         sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#             )
#
#             if event['type'] == 'checkout.session.completed':
#                 session = event['data']['object']
#                 customer_email = session.get("customer_details", {}).get("email", "")
#                 product_id = session.get("metadata", {}).get("product_id")
#
#                 if product_id:
#                     product = Product.objects.get(id=product_id)
#                     send_mail(
#                         subject="Here is your booked package",
#                         message=f"Thank you for your booking. Here are the booking details. The URL is {product.url}",
#                         recipient_list=[customer_email],
#                         from_email="desaipoojan2001@gmail.com"  # Use a valid sender email address
#                     )
#                     print(f"Email sent to {customer_email} for product {product.name}")
#                 else:
#                     print("Product ID not found in session metadata.")
#
#             else:
#                 print(f"Unhandled event type: {event['type']}")
#
#         except ValueError:
#             print("Invalid payload")
#             return HttpResponse(status=400)
#         except stripe.error.SignatureVerificationError:
#             print("Invalid signature")
#             return HttpResponse(status=400)
#
#         return HttpResponse(status=200)
#     else:
#         return HttpResponse(status=405)
#
# def handle_checkout_session(session):
#     customer_email = session.get("customer_details", {}).get("email")
#     product_id = session.get("metadata", {}).get("product_id")
#     product = Product.objects.get(id=product_id)
#
#     send_mail(
#         subject="Your product purchase is successful",
#         message=f"Thank you for your purchase. Here are the booking details. Product Name: {product.name}, URL: {product.url}",
#         recipient_list=[customer_email],
#         from_email=settings.DEFAULT_FROM_EMAIL
#     )
#     print(f"Email sent to {customer_email} for product {product.name}")
#
# class StripeIntentView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             product_id = self.kwargs["pk"]
#             product = Product.objects.get(id=product_id)
#             intent = stripe.PaymentIntent.create(
#                 amount=product.price,
#                 currency='usd'  # assuming USD is the desired currency
#             )
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)})

import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'cad',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='cad',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
