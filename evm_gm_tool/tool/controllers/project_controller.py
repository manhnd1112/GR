from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import(
    Project as ProjectModel, 
    ProjectMember, 
    GroupAccess, 
    UserProfile,
    Utils
)
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm, ProjectViewForm
from tool.utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings

class ProjectController:
    def index(request):
        args = {}
        if(request.GET.get('search')):
            search_term = request.GET.get('search')
            args['search_term'] = search_term            
            project_list = ProjectModel.get_projects_has_access(request.user.id,search_term)            
        else:
            args['search_term'] = ''
            project_list = ProjectModel.get_projects_has_access(request.user.id)
        if(request.GET.get('per-page')):
            page_limit = int(request.GET.get('per-page'))
        else:
            page_limit =  settings.PAGE_LIMIT

        paginator = Paginator(project_list, page_limit) # Show 25 contacts per page
        page = request.GET.get('page')

        projects = paginator.get_page(page)
        args['projects'] = projects
        return render(request, 'tool/project/index.html', args)

    def create(request):
        if not request.user.is_superuser:
            return redirect('tool:error_no_access')
        if request.method == "POST":
            form = ProjectCreationForm(request.POST or None)
            args = {'form': form}                     
            if form.is_valid():
                new_project = form.save()
                members_data = request.POST.get('members')
                if(members_data != '' and members_data is not None):
                    members = json.loads(members_data)
                    ProjectMember.add_member_list(new_project, request.user, members)
                messages.success(request, 'New project created successfully')
                return redirect(reverse('tool:project_edit', args=(new_project.id,)))
            else:
                args['errors'] = form.errors
                return render(request, 'tool/project/create.html', args)
        else: 
            form = ProjectCreationForm(initial={'owner': request.user})
            args = {'form': form}
            return render(request, 'tool/project/create.html', args)
    
    def view(request, id):
        project = get_or_none(ProjectModel, pk=id)
        if project is None:
            return redirect('tool:page_not_found')
        members = ProjectMember.get_member_list(project)
        args = {'project': project, 'member_list': members}
        return render(request, 'tool/project/view.html', args)

    def edit(request, id):
        project = ProjectModel.objects.get(id=id)
        # check has permission edit project
        has_edit_permission = False 
        group_access = ProjectMember.get_group_access(request.user.id, project.id)
        if(group_access != GroupAccess.READ):
            has_edit_permission = True

        if not has_edit_permission:
            return redirect('tool:error_no_access')

        if request.method == "POST":
            form = ProjectEditForm(request.POST,instance=project)
            args = {'form': form, 'project': project}
            if form.is_valid():
                form.save()
                # if(request.POST.get('members') != ''):
                #     member_list = json.loads(request.POST.get('members'))
                #     ProjectMember.update_project_member(project, request.user.id, member_list)                             
                members = ProjectMember.get_member_list(project)
                args['members'] = members
                messages.success(request, 'Project updated successfully')                                    
                return render(request, 'tool/project/edit.html', args)
            else:
                args['errors'] = form.errors
                return render(request, 'tool/project/edit.html', args)
        else: 
            project = ProjectModel.objects.get(id=id)
            form = ProjectEditForm(instance=project)
            members = ProjectMember.get_member_list(project)
            args = {'form': form, 'members': json.dumps(members), 'member_list': members, 'project': project}
            return render(request, 'tool/project/edit.html', args)

    def delete(request, id):
        group_access = ProjectMember.get_group_access(request.user.id, id)        
        if group_access != GroupAccess.SUPERUSER and group_access != GroupAccess.OWNER:
            return redirect('tool:error_no_access')
        project_remove = get_or_none(ProjectModel, pk=id)
        if project_remove is None:
            return redirect('tool:page_not_found')
        project_remove.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('tool:project_index')

            