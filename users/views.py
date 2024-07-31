import json
import regex as re
from users.rules import user_rules
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
#from rating.helpers.json_response import jsonResponse
from django_easy_validation import Validator
from helpers.general import is_ajax
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse as response, HttpResponseRedirect, JsonResponse
from helpers.general import make_pagination

# Create your views here.

@login_required
def index(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request,"users/index.html", context)

@login_required
def create(request):
    # form = UserForm()
    return render(request, "users/create.html")

@never_cache
@login_required    
def store(request):
    data = json.loads(request.body)
    errors = Validator.validate(request, {
        "username": "required|unique:auth_user|max:10|min:4",
        "email" : "required|email"
    })
    
    if errors:
        return JsonResponse(errors, status=422, safe=False)
    
    if errors and is_ajax:
        return JsonResponse(errors, status=422, safe=False)
    
    newData = {
        "password": make_password(data['password']),
        "is_superuser": data['is_superuser'],
        "username": data['username'],
        "last_name": data['last_name'],
        "email": data['email'],
        "is_active": data['is_active'],
        "first_name": data['first_name'],
    }

    data['password'] = make_password(data['password'])
    user = User.objects.create(**newData)
    return response(user)
    # return response(request.POST.get('first_name'))

@login_required
def all(request):
    paginate = request.GET.get('paginate')
    users = User.objects.all().order_by('-id')
    if paginate:
        paginated_data = make_pagination(request, users)
        return JsonResponse(paginated_data, safe=False)
    else:
        users = list(User.objects.all().order_by('-id').values())
        return JsonResponse(users, safe=False)
    
    
    # paginate = request.GET.get('paginate')
    # page = request.GET.get('page')
    # limit=5
    # users = []
    # offset = 0
    # total = User.objects.count()
    # if page:
    #     offset = (int(page)-1)*limit
    # if paginate:
    #     users = list(User.objects.all().order_by('-id').values("id","username","email","first_name","last_name","is_active","is_superuser")[offset:offset+limit])
    #     offset += limit
    #     return JsonResponse({"users": users, "total": total, "per_page":5}, safe=False)
    # else:
    #     users = list(User.objects.all().order_by('-id').values("id","username","email","first_name","last_name","is_active","is_superuser"))
    #     return JsonResponse(users, safe=False)

@require_http_methods(['PUT'])
@login_required
def update(request, user_id):
    data = json.loads(request.body)
    errors = Validator.validate(request, {
        "username": "required|unique:auth_user|max:10|min:6",
        "email" : "required|email"
    })
    
    if errors:
        return JsonResponse(errors, status=422, safe=False)
    
    if errors and is_ajax:
        return JsonResponse(errors, status=422, safe=False)
    
    newData = {
        "is_superuser": data['is_superuser'],
        "username": data['username'],
        "last_name": data['last_name'],
        "email": data['email'],
        "is_active": data['is_active'],
        "first_name": data['first_name'],
    }
    
    if(data['password']):
        newData.update("password", make_password(data['password']))

    data['password'] = make_password(data['password'])
    user = User.objects.filter(id=user_id).update(**newData)
    return response(user)

@login_required
def destroy(request,user_id):
    user = User.objects.filter(id=user_id).delete()
    return JsonResponse('success', safe=False)

# @login_required
# def profile(request, username):
#     user = get_object_or_404(User, username=username)
    
#     if request.method == 'POST':
#         if 'update_profile' in request.POST:
#             profile_form = UserForm(request.POST, request.FILES, instance=user)
#             if profile_form.is_valid():
#                 profile_form.save()
#                 return redirect('profile', username=user.username)
#         elif 'change_password' in request.POST:
#             password_form = CustomPasswordChangeForm(user=user, data=request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)  # Important for keeping the user logged in
#                 return redirect('profile', username=user.username)
#     else:
#         profile_form = UserProfileForm(instance=user)
#         password_form = CustomPasswordChangeForm(user=user)
    
#     context = {
#         'user': user,
#         'profile_form': profile_form,
#         'password_form': password_form,
#     }
#     return render(request, 'users/profile.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES.get('profile_picture')
            user.profile_picture = profile_picture
            user.save()
            return redirect('profile', username=user.username)

        if 'password' in request.POST:
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 and new_password2:
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    return redirect('profile', username=user.username)
                else:
                    return render(request, 'users/profile.html', {'user': user, 'error': 'Passwords do not match'})
        


    return render(request, 'users/profile.html', {'user': request.user})
