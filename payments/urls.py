from django.urls import path
from . import views

urlpatterns = [
    path('test-payment/', views.test_payment, name='test-payment'),
    path('get-pub-key/', views.publishable_key, name='get-pub-key'),
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('checkout-session/', views.create_checkout_session, name='checkout-session'),
]

