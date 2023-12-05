from django.urls import path

from . import views

urlpatterns = [
    path('get-book-list/', views.BookListView.as_view(), name='get-book-list'),
]
