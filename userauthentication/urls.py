from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_new_user, name='registerapi'),
    path('login/', views.login_new_user, name='loginapi'),
    path('logout/', views.logout_user, name='logoutapi'),
]