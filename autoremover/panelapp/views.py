from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def pricing_page(request):
    return render(request, 'panelapp/pricing.html')
