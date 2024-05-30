from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse as response, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
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
        return redirect('/users')
    else:
        return response('error')