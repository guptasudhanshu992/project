from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')

        if email:
            try:
                user = User.objects.get(email=email)
                
                if not sociallogin.is_existing and not user.socialaccount_set.filter(provider=sociallogin.account.provider).exists():
                    raise ImmediateHttpResponse(
                        render(request, "error.html", {
                            "error_title": "Account Already Exists",
                            "error_message": f"An account already exists with the email '{email}' but it is not linked with {sociallogin.account.provider.capitalize()}. Please login using your email and password."
                        }, status=400)
                    )
            except User.DoesNotExist:
                pass
