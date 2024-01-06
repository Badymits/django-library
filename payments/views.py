from django.shortcuts import render
from django.conf import settings
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