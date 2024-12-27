from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            context = {
                'error': 'You must be logged in to access this resource.',
             }
        else:
            user = request.user

            context = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }

        return render(request, 'profile.html', context)
