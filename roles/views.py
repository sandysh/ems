from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission, User
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

@login_required
def index(request):
    groups = Group.objects.all()
        
    group_user_list = []
    for group in groups:
        group_user_list.append({
            'group': group,
        })

    user_groups = [group.name for group in request.user.groups.all()]

    context = {
        'groups': groups,
        'group_user_list': group_user_list,
        'user_groups': user_groups,
    }
    return render(request, 'roles/index.html', context)

def update_role(user, group_id):
    if not group_id:
        return
    group = Group.objects.filter(id=group_id).first()
    if not group:
        return
    if user.groups.filter(id=group.id).exists():
        return
    user.groups.clear()
    user.groups.add(group)



@login_required
def add_role(request):
    permissions = Permission.objects.all()

    if request.method == 'POST':
        group_name = request.POST.get('name')
        selected_permissions = request.POST.getlist('permissions')

        group, created = Group.objects.get_or_create(name=group_name)

        group.permissions.set(Permission.objects.filter(id__in=selected_permissions))

        messages.success(request, 'Role created successfully.')
        return redirect('rolesIndex')

    context = {
        'permissions': permissions,
    }
    return render(request, 'roles/add_role.html', context)


    


@login_required
def edit_role(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    permissions = Permission.objects.all()

    if request.method == 'POST':
        group_name = request.POST.get('name')
        selected_permissions = request.POST.getlist('permissions')

        group.name = group_name
        group.save()

        group.permissions.set(Permission.objects.filter(id__in=selected_permissions))


        messages.success(request, 'Role updated successfully.')
        return redirect('rolesIndex')

    context = {
        'role': group,
        'permissions': permissions,
    }
    return render(request, 'roles/edit_role.html', context)



@login_required
def delete_role(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, 'Role deleted successfully.')
    return redirect('rolesIndex')

    
@login_required
def permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    permissions = group.permissions.all()

    context = {
        'role': group,
        'permissions': permissions,
    }
    return render(request, 'roles/permissions.html', context)


@login_required
@require_http_methods(['GET'])
def all_roles(request):
    roles=Group.objects.all()
    roles_data = [{'id': role.id, 'name': role.name} for role in roles]
    return JsonResponse(roles_data, safe=False)