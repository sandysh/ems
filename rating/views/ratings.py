from django.shortcuts import render

def index(request) :
    return render(request,'backend/ratings/index.html')