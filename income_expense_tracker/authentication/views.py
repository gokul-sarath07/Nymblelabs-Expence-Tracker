from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from validate_email import validate_email
import json


class RegistrationView(View):

    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            "fieldValues": request.POST
        }

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password) < 6:
                        messages.error(request,
                                       "Password must be atleast 6 characters")
                        return render(request, 'authentication/register.html',
                                      context)

                    user = User.objects.create_user(username=username,
                                                    email=email)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Account successfully created")
                    return render(request, 'authentication/register.html')
        else:
            messages.error(request, "Please fill all fields.")
            return render(request, 'authentication/register.html', context)


class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not username.isalnum():
            return JsonResponse({
                'username_error':
                    'Username should only contain alphanumeric characters'
            }, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': "Sorry, that username's taken. Try another?"
            }, status=409)
        return JsonResponse({'username_valid': True}, status=200)


class EmailValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({
                'email_error': 'This email is invalid'
            }, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': 'This email already exists, Please login.'
            }, status=409)
        return JsonResponse({'email_valid': True}, status=200)


class PasswordValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        password = data['password']
        if len(password) < 6:
            return JsonResponse({
                'password_error': 'Passwords must be atleast 6 characters.'
            }, status=400)
        return JsonResponse({'password_error': True}, status=200)


class LoginView(View):

    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('home')
            messages.error(request, "Incorrect credentials, Try again.")
            return render(request, 'authentication/login.html')
        messages.error(request, "Please fill all fields.")
        return render(request, 'authentication/login.html')


class LogoutView(View):

    def post(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('login')
