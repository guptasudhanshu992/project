from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json
import re

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = json.loads(request.body)

        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        password = data.get('password', '').strip()
        password_confirm = data.get('password_confirm', '').strip()
        email = data.get('email', '').strip()

        print(f"first_name: {first_name}, last_name: {last_name}, email: {email}")

        if first_name and (len(first_name) < 3 or len(first_name) > 30):
            return JsonResponse({'error': 'First Name must be between 3 and 30 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            print(password)
            return JsonResponse({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[A-Z]', password):
            return JsonResponse({'error': 'Password must contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[a-z]', password):
            return JsonResponse({'error': 'Password must contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[0-9]', password):
            return JsonResponse({'error': 'Password must contain at least one digit.'}, status=status.HTTP_400_BAD_REQUEST)

        if (password_confirm != password):
            return JsonResponse({'error': 'Password and Confirm Password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return JsonResponse({'error': 'Password must contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        redirect_url="/"
        return JsonResponse({'message': 'User created successfully.', "redirect_url": redirect_url}, status=status.HTTP_201_CREATED)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return JsonResponse({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        redirect_url = "/"

        if user is not None:
            login(request, user)
            return JsonResponse({"detail": "Login successful.", "redirect_url": redirect_url}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message":"Unexpected error occurred.", "redirect_url": redirect_url}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        redirect_url = "/"
        return JsonResponse({"detail": "Logout successful.", "redirect_url": redirect_url}, status=status.HTTP_200_OK)
