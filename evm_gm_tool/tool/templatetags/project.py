from django import template
from ..models import *
register = template.Library()

@register.filter
def get_item(List, i):
    return List[int(i)]

@register.filter
def has_all_permission(user, project):
    group_access = Project.get_group_access(user.id, project.id)
    print(group_access)
    if group_access == GroupAccess.SUPERUSER or group_access == GroupAccess.OWNER:
        return True
    return False

@register.filter
def has_permission_ge_admin(user, project):
    group_access = Project.get_group_access(user.id, project.id)
    print(group_access)
    if group_access == GroupAccess.SUPERUSER or group_access == GroupAccess.OWNER or group_access == GroupAccess.ADMIN:
        return True
    return False


@register.filter
def has_write_permission(user, project):
    group_access = Project.get_group_access(user.id, project.id)
    if group_access != GroupAccess.READ:
        return True
    return False

@register.filter
def get_group_access_as_text(group_access):
    if group_access == GroupAccess.READ:
        return 'Read'
    elif group_access == GroupAccess.WRITE:
        return 'Write'
    elif group_access == GroupAccess.ADMIN:
        return 'Admin'
    elif group_access == GroupAccess.OWNER:
        return 'Owner'
    elif group_access == GroupAccess.SUPERUSER:
        return 'Superuser'