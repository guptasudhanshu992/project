from django.urls import path
from .views import RegisterView, RegisterAPI, LoginView, LoginAPI
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # Views
    path('register/', RegisterView.as_view(), name='register_view'),
    path('login/', LoginView.as_view(), name='login_view'),

    # APIs
    path('api/register/', RegisterAPI.as_view(), name='register_api'),
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]