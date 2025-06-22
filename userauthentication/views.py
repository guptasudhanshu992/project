from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import Roles, UserRoles, UserDetails
from django.contrib.auth.models import Group
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from django.conf import settings
from allauth.socialaccount.models import SocialApp, SocialLogin
from django.contrib.sites.models import Site
import json
import time
import re
import random
import string
import requests

User = get_user_model()

def register_new_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            confirm_password = data.get('confirm_password', '').strip()
            source = data.get('source', 'Email').strip()
            
            try:
                role = Roles.objects.get_or_create(name='Learner')
            except Roles.DoesNotExist:
                raise ValueError(f"Role 'Learner' does not exist.")
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                return JsonResponse({'message': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

            if not re.search(r'[A-Z]', password):
                return JsonResponse({'message': 'Password must contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

            if not re.search(r'[a-z]', password):
                return JsonResponse({'message': 'Password must contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

            if not re.search(r'[0-9]', password):
                return JsonResponse({'message': 'Password must contain at least one digit.'}, status=status.HTTP_400_BAD_REQUEST)

            if (confirm_password != password):
                return JsonResponse({'message': 'Password and Confirm Password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                return JsonResponse({'message': 'Password must contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(email=email, password=password, source=source)
            
            #UserRoles.objects.create(user_id=user.user_id, role=role.role_id)
            UserDetails.objects.create(user=user)
            
            group, created = Group.objects.get_or_create(name='Learner')
            user.groups.add(group)
            
            login(request, user)
            #send_welcome_email(request, email, firstname, lastname)
            
            redirect_url="/"
            return JsonResponse({'message': 'User created successfully.', "redirect_url": redirect_url}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)

def login_new_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        user = authenticate(request, email=email, password=password)
        redirect_url='/'
    
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Welcome Back!', 'redirect_url': redirect_url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password...'}, status=401)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout Successful!', 'redirect_url': '/'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)