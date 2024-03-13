from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

def customer_required(function):
    def _function(request, *args, **kwargs):
        if request.user.is_staff:
            messages.info(request, 'You have to be a customer to access this page. \nYou can create an account if you don\'t have one.')
            logout(request)
            next = request.path
            return HttpResponseRedirect(reverse('Login') + f'?next={next}')
        return function(request, *args, **kwargs)

    return _function

def login_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            next = request.path
            return HttpResponseRedirect(reverse('Login') + f'?next={next}')
        return function(request, *args, **kwargs)

    return _function
