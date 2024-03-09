from django.shortcuts import render, redirect
from .decorators import login_required, staff_required, admin_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from database.models import *

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
    if request.method == "POST":
        if request.POST.get('form_name') == "add_process":
            process_name = request.POST.get('process_name')
            try:
                process = FileProcess.objects.create(name=process_name)
                messages.success(request, f"File process '{process.name}' has been added successfully!")
            except:
                messages.error(request, "File process could not be saved!")

        elif request.POST.get('form_name') == "update_process":
            process_id = int(request.POST.get('process_id'))
            process_name = request.POST.get('process_name')
            try:
                process = FileProcess.objects.get(id=process_id)
                old_name = process.name
                process.name = process_name
                process.save()
                messages.success(request, f"File process '{old_name}' has been updated as '{process.name}' successfully!")
            except:
                messages.error(request, "File process could not be updated!")
        
        elif request.POST.get('form_name') == "add_tool":
            tool_name = request.POST.get('tool_name')
            try:
                tool = ConnectionTool.objects.create(name=tool_name)
                messages.success(request, f"Connection tool '{tool.name}' has been added successfully!")
            except:
                messages.error(request, "Connection tool could not be saved!")

        elif request.POST.get('form_name') == "update_tool":
            tool_id = int(request.POST.get('tool_id'))
            tool_name = request.POST.get('tool_name')
            try:
                tool = ConnectionTool.objects.get(id=tool_id)
                old_name = tool.name
                tool.name = tool_name
                tool.save()
                messages.success(request, f"Connection tool '{old_name}' has been updated as '{tool.name}' successfully!")
            except:
                messages.error(request, "Connection tool could not be updated!")

    context = {
        'page_title': 'Customer Options',
        'processes': FileProcess.objects.all().order_by('name'),
        'tools': ConnectionTool.objects.all().order_by('name'),
    }
    return render(request, 'panelapp/pages/customer_options.html', context)
