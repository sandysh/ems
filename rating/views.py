from django.shortcuts import render
from django.http import HttpResponse as response
from .views import user
# Create your views here.

def index(request):
    return render(request,"backend/dashboard.html")