# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='user_login'),
    # Add more URLs for other user-related views
]