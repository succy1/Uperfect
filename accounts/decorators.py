from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.urls import reverse

def subscription_required(subscription_types=None):
    """
    Decorator to check if user has required subscription access.
    
    Args:
        subscription_types (list, optional): List of required subscription tier names.
                                           If None, any subscription is sufficient.
    
    Usage:
        @subscription_required()  # Requires any subscription
        @subscription_required(['Premium', 'Pro'])  # Requires Premium or Pro subscription
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this feature.')
                return redirect('login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                messages.warning(request, 'Please complete your profile first.')
                return redirect('onboarding')
            
            # Get user's subscription
            user_subscription = request.user.profile.subscription_tier
            
            # If no subscription_types specified, just check if user has any subscription
            if subscription_types is None:
                if user_subscription is None:
                    messages.warning(
                        request, 
                        'This feature requires a subscription. Please upgrade your plan.'
                    )
                    return redirect('pricing')
                return view_func(request, *args, **kwargs)
            
            # Check if user's subscription is in allowed types
            if user_subscription and user_subscription.name in subscription_types:
                return view_func(request, *args, **kwargs)
            
            messages.warning(
                request, 
                f'This feature requires one of these subscriptions: {", ".join(subscription_types)}'
            )
            return redirect('pricing')
            
        return _wrapped_view
    return decorator