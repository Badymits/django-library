from django.urls import path
from . import views

urlpatterns = [
    path('test-payment/', views.test_payment, name='test-payment'),
]

