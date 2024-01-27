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

@api_view(['GET'])
def publishable_key(request):
    response_data={
        'pub_key': settings.PUB_KEY
    }
    #print(data.pub_key)
    return Response( data=response_data)

# creating a payment intent which is initiates the payment process for checking out the items in the front end
@api_view(['GET'])
def create_payment_intent(request):
    try:
        # print(f'total amount: {request.GET.get("total_amount")}')
        # total = format(float(request.GET.get("total_amount")) / 100, ".2f")
        # print(total)
        payment_intent = stripe.PaymentIntent.create(
            amount=request.GET.get("total_amount"),
            currency='PHP',
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

def create_item_list(*args):
    print('Eto yung args natin erp: ',*args)
    book_items_list = []
    for index in range(len(args)):
        for k, v in args[index].items():
            if k == 'book_price':
                book_items_list.append({
                    'price': v,
                    'quantity': 1,
                    
                })
            print(f'Key: {k} || Value: {v}')
            #print(item)
    #return book_item_list

@api_view(['POST'])
def create_checkout_session(request):

    book_dict = request.data.items()
    book_items_list = []
    
    print(book_dict)
    for k,v in book_dict:
        if k == 'email':
            user_email = v
        if k == 'items':
            create_item_list(*v)
        
    print(f'user email: {user_email}')
    #print(f'items: {book_items_list[0]}')
    
    # for index in range(len(book_items_list[0])):
    #     for item in book_items_list[0][index].values():
    #         print(item)
            
            
    # checkout_session = stripe.checkout.Session.create(
    #     line_items=[{
        #   price: request.data.items
        # }],
    #     payment_method_types=["card"]
    # )
    return Response({'message': 'received ahahaha'})