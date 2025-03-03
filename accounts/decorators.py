from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def doctor(view_func):
    """Decorator to allow only doctors to access a view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_doctor:
            return view_func(request, *args, **kwargs)
        return redirect('forbidden')  # Redirect to 403 page
    return _wrapped_view


def patient(view_func):
    """Decorator to allow only patients to access a view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_patient:
            return view_func(request, *args, **kwargs)
        return redirect('forbidden')  # Redirect to 403 page
    return _wrapped_view


def hospital(view_func):
    """Decorator to allow only hospitals to access a view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_hospital:
            return view_func(request, *args, **kwargs)
        return redirect('forbidden')  # Redirect to 403 page
    return _wrapped_view
