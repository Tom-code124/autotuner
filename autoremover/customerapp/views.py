from django.shortcuts import render

# Create your views here.

def dtc_search(request):
    context = {'username': 'yunus'}
    return render(request, "pages/dtc_search.html", context)