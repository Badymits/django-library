from django.urls import path

from . import views

urlpatterns = [
    path('get-book-list/', views.BookListView.as_view(), name='get-book-list'),
    path('get-book-detail/<int:pk>/', views.BookDetailView.as_view(), name='get-book-detail')
]
