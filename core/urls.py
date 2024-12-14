from django.urls import path
from .views import HomeView, ProfileView


urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('profile/', ProfileView.as_view(), name='profile'),

]