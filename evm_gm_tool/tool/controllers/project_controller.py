from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import Project as ProjectModel, ProjectMember, GroupAccess
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm
from tool.utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class ProjectController:
    def index(request):
        project_list = ProjectModel.objects.all()
        paginator = Paginator(project_list, 3) # Show 25 contacts per page

        page = request.GET.get('page')
        projects = paginator.get_page(page)
        return render(request, 'tool/project/index.html', {'projects': projects})

    def create(request):
        if request.method == "POST":
            form = ProjectCreationForm(request.POST)
            args = {'form': form}                     
            if form.is_valid():
                new_project = form.save()
                members_data = request.POST.get('members')
                print(members_data)
                if(members_data != '' and members_data is not None):
                    members = json.loads(members_data)
                    ProjectMember.add_member_list(new_project, request.user, members) 
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
        args = {'project': project}
        return render(request, 'tool/project/view.html', args)

    def edit(request, id):
        project = ProjectModel.objects.get(id=id)
        # check has permission edit project
        is_owner_or_admin_or_supperuser = False or request.user.is_superuser
        group_access = ProjectMember.get_group_access(request.user.id, project.id)
        if(group_access == GroupAccess.OWNER or group_access == GroupAccess.ADMIN):
            is_owner_or_admin_or_supperuser = True

        if not is_owner_or_admin_or_supperuser:
            return redirect('tool:error_no_access')

        if request.method == "POST":
            form = ProjectEditForm(request.POST,instance=project)
            args = {'form': form}
            if form.is_valid():
                form.save()
                # if(request.POST.get('members') != ''):
                #     member_list = json.loads(request.POST.get('members'))
                #     ProjectMember.update_project_member(project, request.user.id, member_list)                             
                members = ProjectMember.get_member_list(project)
                args['members'] = members                    
                return render(request, 'tool/project/edit.html', args)
            else:
                print(ProjectMember.get_group_access(request.user.id, project_id))
                args['errors'] = form.errors
                return render(request, 'tool/project/edit.html', args)
        else: 
            project = ProjectModel.objects.get(id=id)
            form = ProjectEditForm(instance=project)
            members = ProjectMember.get_member_list(project)
            args = {'form': form, 'members': json.dumps(members)}
            return render(request, 'tool/project/edit.html', args)

    def delete(request, id):
        is_admin = request.user.is_superuser
        if not is_admin:
            return redirect('tool:error_no_access')
        project_remove = get_or_none(ProjectModel, pk=id)
        if project_remove is None:
            return redirect('tool:page_not_found')
        print(project_remove)
        project_remove.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('tool:project_index')

    # def ajax_upload_csv(request):
    #     if request.method == 'POST':
    #         file_input = request.FILES['file']
    #         data = ProjectController.handle_uploaded_file(file_input)
    #         return JsonResponse({'data': data})

    # def handle_uploaded_file(f):
    #     workbook = xlrd.open_workbook(file_contents=f.read())
    #     sheet = workbook.sheet_by_index(0)
    #     nrows = sheet.nrows - 1
    #     ncols = sheet.ncols
    #     data = []
    #     for col in range(sheet.ncols):
    #         data.append(sheet.col_values(col))
    #     for i in range(len(data)):
    #         data[i].remove(data[i][0])
    #     return data
            