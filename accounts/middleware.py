from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

class ProfileCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if isinstance(request.user, AnonymousUser):
            return self.get_response(request)

        if request.user.is_authenticated:
            current_url = resolve(request.path_info).url_name
            excluded_urls = ['onboarding', 'logout', 'login', 'admin', 'static']
            
            # Don't redirect if user is accessing excluded URLs
            if current_url in excluded_urls:
                return self.get_response(request)
            
            # Check if user has a profile
            try:
                profile = request.user.profile
            except:
                # If no profile exists, redirect to onboarding
                if current_url != 'onboarding':
                    return redirect('onboarding')

        return self.get_response(request)