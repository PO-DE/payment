from typing import Any

import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = "Success.html"

class CancelView(TemplateView):
    template_name = "Cancel.html"



class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs: Any):
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
        print(product)
        YOUR_DOMAIN = "http://127.0.0.1:8000/"

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                        {
                            'price_data': {
                                'currency': 'cad',
                                'unit_amount': product.price,
                                'product_data': {
                                    'name':product.name,
                                },
                            },
                            'quantity': 1,
                        },
                    {
                        # Replace 'YOUR_PRICE_ID' with the actual Price ID of the product you want to sell
                        'price': 'price_1OoDr8LzuIIGxeVezXtEPNyE',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return redirect(checkout_session.url)

# Create your views here.


# Create your views here.
