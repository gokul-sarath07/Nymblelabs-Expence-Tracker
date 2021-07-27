from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import RegistrationView, UsernameValidationView, \
                   EmailValidationView, PasswordValidationView, \
                   LoginView, LogoutView


"""Url patterns for authentication views."""
urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate-email'),
    path('validate-password', csrf_exempt(PasswordValidationView.as_view()),
         name='validate-password'),
]
