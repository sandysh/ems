from django import template
from django.contrib.auth.models import Group, Permission

register = template.Library()

@register.filter
def has_group_permission(user,permission_codename):
   
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        group=user.groups.all().first()
        permission = Permission.objects.get(codename=permission_codename)
        return group and group.permissions.filter(id=permission.id).exists()
    except (Group.DoesNotExist, Permission.DoesNotExist, ValueError):
        return False
