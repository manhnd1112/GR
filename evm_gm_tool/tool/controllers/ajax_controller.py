from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import Project as ProjectModel, ProjectMember, GroupAccess, Utils
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm
from tool.utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class AjaxController:  
    def search_user(request):
        keyword = request.GET.get('keyword')
        # users = User.objects.filter(username__regex=r'^.*{}.*$'.format(keyword))
        users = User.objects.filter(username__icontains = keyword)
        # users_list = list(users.values_list('id', 'username'))
        user_tuple_list = list(users.values_list('id', 'username'))
        user_list = []
        for user_tuple in user_tuple_list:
            user = {}
            user['id'] = user_tuple[0]
            user['username'] = user_tuple[1]
            user['avatar-url'] = Utils.get_avatar_url_by_user_id(user_tuple[0])
            user_list.append(user)
        return JsonResponse({'users': user_list})

    def add_project_memger(request):
        if request.method == 'GET':
            project_id = request.GET.get('project_id')
            user_id = request.GET.get('user_id')
            group_access = request.GET.get('group_access')
            add_status = ProjectMember.add_project_member(request.user, project_id, user_id, group_access)
            if add_status == -1:
                return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
            elif add_status == -2:
                return JsonResponse({'status': 404, 'err': "Project member or Project not found"})
            elif add_status == -3:
                return JsonResponse({'status': 500, 'err': "Member already added as project member"})
            else:
                return JsonResponse({'status': 200, 'id': add_status})
        else:
            return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

    def remove_project_member(request):
        if request.method == 'GET':
            project_id = request.GET.get('project_id')
            project_member_id = request.GET.get('project_member_id')
            remove_status = ProjectMember.remove_project_member(request.user, project_id, project_member_id)
            if remove_status == -1:
                return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
            elif remove_status == -2:
                return JsonResponse({'status': 404, 'err': "Project member not found"})
            else:
                return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

    def update_group_access(request):
        if request.method == 'GET':
            project_id = request.GET.get('project_id')
            project_member_id = request.GET.get('project_member_id')
            group_access = request.GET.get('group_access')
            update_status = ProjectMember.update_group_access(request.user, project_member_id, group_access)
            if update_status == -1:
                return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
            elif update_status == -2:
                return JsonResponse({'status': 404, 'err': "Project member not found"})
            else:
                return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

    def get_project_detail(request):
        if request.method == 'GET':
            project_id = request.GET.get('project_id')
            project = get_or_none(ProjectModel, pk=project_id)
            if project is None:
                return JsonResponse({'status': 404, 'err': "Project not found"})
            data = {}
            data["pd"] = project.pd
            data["budget"] = project.budget
            data["status"] = project.status
            return JsonResponse({'status': 200, 'data': data})
        else:
            return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})