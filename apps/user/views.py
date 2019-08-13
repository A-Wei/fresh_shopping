from django.shortcuts import render

# Create your views here.
def register(request):
    """Render registration page"""
    return render(request, 'register.html')
