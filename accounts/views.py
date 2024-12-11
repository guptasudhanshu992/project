from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        password = request.data.get('password', '').strip()
        password_confirm = request.data.get('password_confirm', '').strip()
        email = request.data.get('email', '').strip()

        if first_name and (len(first_name) < 3 or len(first_name) > 30):
            return Response({'error': 'First Name must be between 3 and 30 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            try:
                validate_email(email)
            except ValidationError:
                return Response({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[A-Z]', password):
            return Response({'error': 'Password must contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[a-z]', password):
            return Response({'error': 'Password must contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[0-9]', password):
            return Response({'error': 'Password must contain at least one digit.'}, status=status.HTTP_400_BAD_REQUEST)

        if (password_confirm != password):
            return Response({'error': 'Password and Confirm Password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return Response({'error': 'Password must contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

class LoginAPI(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            redirect_url = request.data.get("next", "/")
            return Response(
                {
                    "tokens": response.data,
                    "redirect_url": redirect_url,
                },
                status=status.HTTP_200_OK,
            )

        return response