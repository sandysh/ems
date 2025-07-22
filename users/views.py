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
from logs.utils import log_action
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

    # Log user creation
    log_action(
        action="User Created",
        model="User",
        action_by=request.user,
        action_to=user,
        old={},
        new={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "group_id": group.id if group else None,
            "supervisor_id": supervisor_id
        }
    )
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
    old_status = user.is_active
    user.is_active = status
    user.save()

    # Log user status change
    log_action(
        action="User Status Changed",
        model="User",
        action_by=request.user,
        action_to=user,
        old={"is_active": old_status},
        new={"is_active": user.is_active}
    )

    return response(status)

@require_http_methods(['PUT'])
def update(request, user_id):
    data = json.loads(request.body)

    # Fetch old user data before update
    old_user = User.objects.get(id=user_id)
    old_data = {
        "user_id": old_user.id,
        "username": old_user.username,
        "email": old_user.email,
        "is_active": old_user.is_active,
        "is_superuser": old_user.is_superuser,
        "first_name": old_user.first_name,
        "last_name": old_user.last_name,
        "group_id": old_user.groups.first().id if old_user.groups.exists() else None,
        "supervisor_id": getattr(getattr(old_user, 'userprofile', None), 'supervisor_id', None)
    }

    newData = {
        "is_superuser": data['is_superuser'],
        "username": data['username'],
        "last_name": data['last_name'],
        "email": data['email'],
        "is_active": data['is_active'],
        "first_name": data['first_name'],
    }

    User.objects.filter(id=user_id).update(**newData)
    user = User.objects.get(id=user_id)
    group_value = data['groups']
    if isinstance(group_value, list):
        group_id = int(group_value[0]) if group_value else None
    else:
        group_id = int(group_value)
    if group_id:
        update_role(user, group_id)

    supervisor_id = data.get('supervisor_id')
    if supervisor_id is not None:
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.supervisor_id = supervisor_id
        profile.save()

    # Log user update with old and new data
    log_action(
        action="User Updated",
        model="User",
        action_by=request.user,
        action_to=user,
        old=old_data,
        new={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "group_id": group_id,
            "supervisor_id": supervisor_id
        }
    )

    return response(user)

@login_required
def destroy(request,user_id):
    user = User.objects.filter(id=user_id).delete()

    # Log user deletion
    log_action(
        action="User Deleted",
        model="User",
        action_by=request.user,
        action_to=user,
        old={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        new={}
    )

    return JsonResponse('success', safe=False)


@login_required
@require_http_methods(['PUT'])
def updateUserPassword(request, user_id):
    data = json.loads(request.body)
    user = User.objects.filter(id=user_id).update(password=make_password(data['new_password']))

    # Log password change
    log_action(
        action="User Password Changed",
        model="User",
        action_by=request.user,
        action_to=user,
        old={},
        new={"user_id": user.id}
    )

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