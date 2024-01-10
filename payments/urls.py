from django.urls import path
from . import views

urlpatterns = [
    path('test-payment/', views.test_payment, name='test-payment'),
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
]

