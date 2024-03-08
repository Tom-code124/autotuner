from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

def admin_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.info(request, 'You have to be an admin member to access this page.')
            logout(request)
            next = request.path
            return HttpResponseRedirect(reverse('Panel Login') + f'?next={next}')
        return function(request, *args, **kwargs)

    return _function

def staff_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.info(request, 'You have to be a staff member to access this page. \nYou can request an account from your administrator if you don\'t have one.')
            logout(request)
            next = request.path
            return HttpResponseRedirect(reverse('Panel Login') + f'?next={next}')
        return function(request, *args, **kwargs)

    return _function

def login_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'You have to be logged in to access this page.')
            next = request.path
            return HttpResponseRedirect(reverse('Panel Login') + f'?next={next}')
        return function(request, *args, **kwargs)

    return _function
