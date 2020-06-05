from django.shortcuts import render, redirect
from .models import Community, Comments
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import upload_and_save
# Create your views here.

def index(request):
    return render(request, 'home/index.html')

def login(request):
    if request.method == 'POST':
        found_user = auth.authenticate(
            username = request.POST['username'],
            password = request.POST['password']
        )
        if found_user is None:
            error = 'Incorrect ID or Password'
            return render(request, 'registration/login.html', {'error': error})
            
        auth.login(request, found_user, backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect(request.GET.get('next', '/'))
    return render(request, 'registration/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def start(request):
    return render(request, 'login.html')