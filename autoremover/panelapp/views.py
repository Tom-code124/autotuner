from django.shortcuts import render, redirect
from .decorators import login_required, staff_required, admin_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def login_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/panel/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.POST.get('next'):
            redirect_url = request.POST.get('next')
        else:
            redirect_url = "/panel/"
        
        print(redirect_url)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_url)

        else:
            messages.error(request, "Invalid username or password!")
            if redirect_url != "/panel/":
                print("reverse:")
                print(reverse('Panel Login'))
                return redirect(reverse('Panel Login') + f'?next={redirect_url}')


    context = {
        'page_title': 'Panel Login',
        'styling_files': [],
        'script_files': [],
        }
    
    return render(request, "panelapp/pages/panel_login.html", context)

@login_required
@staff_required
def logout_view(request):
    logout(request)
    return redirect('Panel Login')

@login_required
@admin_required
def pricing_page(request):
    return render(request, 'panelapp/pages/pricing.html')

@login_required
@admin_required
def customer_options(request):
    return render(request, 'panelapp/pages/customer_options.html')
