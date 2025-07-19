import json
import regex as re
from users.rules import user_rules
from django.contrib.auth.models import User,Group
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from helpers.general import is_ajax
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse as response, HttpResponseRedirect, JsonResponse
from helpers.general import make_pagination,make_serialized_pagination
from django.http import HttpResponse
from serializers.users_serializers import UserSerializer
from roles.views import update_role
from userprofile.models import UserProfile
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
@require_http_methods(["POST"])  
def store(request):
    data = json.loads(request.body)
    serializer =UserSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=422, safe=False)
    
    if not serializer.is_valid and is_ajax:
        return JsonResponse(serializer.errors, status=422, safe=False)
    
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
    try:
        group_id = int(data['group'])
        group = Group.objects.get(id=group_id)
    except (KeyError, ValueError, Group.DoesNotExist):
        group = Group.objects.filter(name="User").first()
        if not group:
            # Optionally, create the group if it doesn't exist
            group = Group.objects.create(name="User")
    user.groups.add(group)

     # Update supervisor in UserProfile
    supervisor_id = data.get('supervisor_id')
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.supervisor_id = supervisor_id
    profile.save()

    return response(user)
    # return response(request.POST.get('first_name'))

@login_required
def all(request):
    paginate = request.GET.get('paginate')
    users_data = User.objects.all().exclude(is_superuser=True).order_by('-id')
    users = UserSerializer(users_data, many=True)
    if  paginate:
        paginated_data = make_serialized_pagination(request, users_data,UserSerializer)
        return JsonResponse(paginated_data, safe=False)
    else:
        return JsonResponse(users.data, safe=False)
    
    
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


def updateUserStatus(request, user_id):
    user = User.objects.get(id=user_id)
    status = False if user.is_active == True else True
    user.is_active = status
    user.save()
    return response(status)

@require_http_methods(['PUT'])
@login_required
def update(request, user_id):
    data = json.loads(request.body)
    # errors = Validator.validate(request, {
    #     "username": "required|unique:auth_user|max:10|min:6",
    #     "email" : "required|email"
    # })
    
    # if errors:
    #     return JsonResponse(errors, status=422, safe=False)
    
    # if errors and is_ajax:
    #     return JsonResponse(errors, status=422, safe=False)
    
    newData = {
        "is_superuser": data['is_superuser'],
        "username": data['username'],
        "last_name": data['last_name'],
        "email": data['email'],
        "is_active": data['is_active'],
        "first_name": data['first_name'],
    }
    
    # if(data['password']):
    #     newData.update("password", make_password(data['password']))

    # data['password'] = make_password(data['password'])
    
    User.objects.filter(id=user_id).update(**newData)
    user = User.objects.get(id=user_id)
    group_value = data['groups']
    if isinstance(group_value, list):
        group_id = int(group_value[0]) if group_value else None
    else:
        group_id = int(group_value)
    if group_id:
        update_role(user, group_id)

    #updating sepervisor
    supervisor_id = data.get('supervisor_id')
    if supervisor_id is not None:
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.supervisor_id = supervisor_id
        profile.save()
        
        return response(user)

@login_required
def destroy(request,user_id):
    user = User.objects.filter(id=user_id).delete()
    return JsonResponse('success', safe=False)


@login_required
@require_http_methods(['PUT'])
def updateUserPassword(request, user_id):
    data = json.loads(request.body)
    user = User.objects.filter(id=user_id).update(password=make_password(data['new_password']))
    return JsonResponse({"status": 'success'}, safe=False)


@login_required
@require_http_methods(['GET'])
def all_users(request):
    users = User.objects.all().order_by('-id')
    data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse(data, safe=False)



    group=Group.objects.get(id=group_id)
    if user and group:
        user.groups.add(group)


@login_required
def supervisors(request):
    """Get all users with supervisor role"""
    try:
        supervisor_group = Group.objects.get(name='supervisor')
        supervisors = User.objects.filter(groups=supervisor_group).values('id', 'first_name', 'last_name', 'email')
        return JsonResponse(list(supervisors), safe=False)
    except Group.DoesNotExist:
        return JsonResponse([], safe=False)