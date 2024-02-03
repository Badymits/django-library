from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user-profile/<str:username>/', views.AccountDetailView.as_view(), name='user-profile'),
    path('user-list/', views.userList, name='user-list'),
    path('user-edit-profile/<str:username>/', views.EditAccountView.as_view(), name='user-edit-profile'),
]


