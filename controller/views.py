from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse as response, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def auth_check(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('/attendance')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/login')

def login_user(request):
    return render(request, 'auth/login.html')

@require_http_methods('POST')
def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request, user)
        if not request.user.is_superuser:
            return redirect('/attendance')
        else:
            return redirect('/dashboard')
    else:
        messages.error(request, "Wrong credentials, please try again",extra_tags="alert alert-danger text-white")
        return redirect('/login')
    

@login_required()
def logout_user(request):
    logout(request)
    return redirect('/login')