from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import stripe

# Create your views here.


stripe.api_key = settings.SECRET_KEY
#print(stripe.api_key)

@api_view(['POST', 'GET'])
def test_payment(request):
    
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com'
    )
    
    return Response(status=200, data=test_payment_intent)

def calculate_cart_amount(items):
    
    amount = 0
    # for i in items:
    #     amount += i.price
    
    return amount

# creating a payment intent which is initiates the payment process for checking out the items in the front end
@api_view(['GET'])
def create_payment_intent(request):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=20000,
            currency='php',
            automatic_payment_methods={'enabled': True}
        )
        
        response_data={
            'client_secret': payment_intent
        }
        
        return Response(data=response_data)
    
    except stripe.error.StripeError as e:
        return JsonResponse({'error': {'message': str(e)}})
    except Exception as e:
        return JsonResponse({'error': {'message': str(e)}})