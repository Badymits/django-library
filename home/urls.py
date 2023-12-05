from django.urls import path

from . import views

urlpatterns = [
    path('get-book-list/', views.BookList.as_view(), name='get-book-list'),
]
