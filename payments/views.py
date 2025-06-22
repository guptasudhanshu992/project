from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    return render(request, 'checkout.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Example Product',
                },
                'unit_amount': 20000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return redirect(session.url, code=303)

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
