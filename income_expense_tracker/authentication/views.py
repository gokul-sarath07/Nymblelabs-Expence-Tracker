from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from validate_email import validate_email
import json



class RegistrationView(View):
    """This class provides functions to work with registration."""

    def get(self, request):
        """This function renders the registration page."""

        return render(request, 'authentication/register.html')

    def post(self, request):
        """This function accepts the registration form data."""

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # variable value mapping that is passed to the registration template.
        context = {
            "fieldValues": request.POST
        }

        # Checks if user has all fields filled.
        if username and email and password:
            # Checks if username already exists in database.
            if not User.objects.filter(username=username).exists():
                # Checks if email already exists in database.
                if not User.objects.filter(email=email).exists():
                    # Checks if password length is less than 6 characters.
                    if len(password) < 6:
                        # Sends error message to user for short password.
                        messages.error(request,
                                       "Password must be atleast 6 characters")
                        # Returns the registration page.
                        return render(request, 'authentication/register.html',
                                      context)

                    # Creates a user object to be saved in database.
                    user = User.objects.create_user(username=username,
                                                    email=email)
                    # Sets the user password.
                    user.set_password(password)
                    # Saves the user to database.
                    user.save()
                    # Sends success message to user for account created.
                    messages.success(request, "Account successfully created")
                    # Directs to login page.
                    return render(request, 'authentication/login.html')
        else:
            # Sends error message to user for empty fields.
            messages.error(request, "Please fill all fields.")
            # Returns the registration page.
            return render(request, 'authentication/register.html', context)


class UsernameValidationView(View):
    """This class is an API View for username validation."""

    def post(self, request):
        """
        - Checks if username is alphanumeric and it doesn't exists in database.
        """

        data = json.loads(request.body)  # gets data from request.
        username = data['username']  # gets username from data.

        # Checks if username is not alphanumeric.
        if not username.isalnum():
            return JsonResponse({
                'username_error':
                    'Username should only contain alphanumeric characters'
            }, status=400)

        # Checks if username already exists in database.
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': "Sorry, that username's taken. Try another?"
            }, status=409)

        # Returns valid username response.
        return JsonResponse({'username_valid': True}, status=200)


class EmailValidationView(View):
    """This class is an API View for email validation."""

    def post(self, request):
        """
        - Checks if email is valid and it doesn't exists in database.
        """

        data = json.loads(request.body)  # gets data from request.
        email = data['email']  # gets email from data.

        # Checks if email is not valid.
        if not validate_email(email):
            return JsonResponse({
                'email_error': 'This email is invalid'
            }, status=400)

        # Checks if email doesn't already exists in database.
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': 'This email already exists, Please login.'
            }, status=409)

        # Returns valid email response.
        return JsonResponse({'email_valid': True}, status=200)


class PasswordValidationView(View):
    """This class is an API View for password validation."""

    def post(self, request):
        """
        - Checks if password is atleast 6 characters.
        """

        data = json.loads(request.body)  # gets the data from request.
        password = data['password']  # gets password from data.

        # Checks if password length is less than 6 characters.
        if len(password) < 6:
            return JsonResponse({
                'password_error': 'Passwords must be atleast 6 characters.'
            }, status=400)

        # Returns valid password response.
        return JsonResponse({'password_error': True}, status=200)


class LoginView(View):
    """This class provides functions to work with login."""

    def get(self, request):
        """This function renders the login page."""

        return render(request, 'authentication/login.html')

    def post(self, request):
        """This function accepts the login form data."""

        username = request.POST['username']  # gets username from request.
        password = request.POST['password']  # gets password from request.

        # Checks if both fields are filled.
        if username and password:
            # Creates user object with given credentials.
            user = authenticate(username=username, password=password)
            # Checks if password is valid for the given user.
            if user:
                # Logs in the user.
                login(request, user)
                # Sends success message to user.
                messages.success(request, "You are now logged in.")
                # redirects them to the home page.
                return redirect('home')

            # Sends error message to user for invalid credentials.
            messages.error(request, "Incorrect credentials, Try again.")
            return render(request, 'authentication/login.html')

        # Sends error message to user for empty fields.
        messages.error(request, "Please fill all fields.")
        return render(request, 'authentication/login.html')


# This view can be accessed only after logging in.
class LogoutView(LoginRequiredMixin, View):
    """This class provides function to work with logout."""

    def post(self, request):
        """Logs out the current user."""

        logout(request)  # Logs out current user.
        # Sends success message to user for successfully logout.
        messages.success(request, "You have successfully logged out.")
        return redirect('login')
