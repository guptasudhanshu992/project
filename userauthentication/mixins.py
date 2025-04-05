from django.shortcuts import redirect

class RedirectAuthenticatedUserMixin:
    """Redirects authenticated users to a specified URL."""
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
