from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from .models import Project as ProjectModel, ProjectMember, GroupAccess
from .forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm
from .utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .controllers.user_controller import *
from .controllers.user_profile_controller import *
from .controllers.project_controller import *
from .controllers.estimate_controller import *
from .controllers.common_controller import *
from .controllers.ajax_controller import *

# Create your views here.
class Dashboard:
    def index(request):
        number_user = User.objects.all().count()
        number_project = len(ProjectModel.get_projects_has_access(request.user.id))
        return render(request, 'tool/dashboard/index.html', {'number_user': number_user, 'number_project': number_project})
    
    def error_no_access(request):
        return render(request, 'tool/dashboard/no_access.html')        
    
    def page_not_found(request):
        return render(request, 'tool/dashboard/not_found.html')

# class UserController:
#     def index(request):
#         user_list = User.objects.all()
#         paginator = Paginator(user_list, 3) # Show 25 contacts per page

#         page = request.GET.get('page')
#         users = paginator.get_page(page)
#         return render(request, 'tool/user/index.html', {'users': users})

#     def create(request):
#         is_admin = request.user.is_superuser
#         if not is_admin:
#             return redirect('tool:error_no_access')

#         if request.method == "POST":
#             form = UserCreateForm(request.POST)
#             args = {'form': form}    
#             if form.is_valid():
#                 new_user = form.save()
#                 return redirect(reverse('tool:user_edit', args=(new_user.id,)))
#             else:
#                 args['errors'] = form.errors
#                 return render(request, 'tool/user/create.html', args)
#         else: 
#             form = UserCreateForm()
#             args = {'form': form}
#             return render(request, 'tool/user/create.html', args)

#     def edit(request, id):
#         is_admin = request.user.is_superuser
#         if not is_admin:
#             return redirect('tool:error_no_access')
#         user_edit = get_or_none(User, pk=id)
#         if user_edit is None:
#             return redirect('tool:page_not_found')
#         if request.method == "POST":
#             form = UserEditForm(request.POST, instance=user_edit)                
#             if form.is_valid():
#                 user_edit = form.save()                  
#                 return redirect(reverse('tool:user_edit', args=(user_edit.id,)))
#             else:
#                 args = {'errors': form.errors, 'form': form}
#                 return render(request, 'tool/user/edit.html', args)
#         else: 
#             form = UserEditForm(instance=user_edit)
#             args = {'form': form}
#             return render(request, 'tool/user/edit.html', args)

#     def delete(request, id):
#         is_admin = request.user.is_superuser
#         if not is_admin:
#             return redirect('tool:error_no_access')
#         user_remove = get_or_none(User, pk=id)
#         if user_remove is None:
#             return redirect('tool:page_not_found')
#         user_remove.delete()
#         messages.success(request, 'User deleted successfully.')
#         return redirect('tool:user_index')

#     def ajax_search(request):
#         keyword = request.GET.get('keyword')
#         print(keyword)
#         # users = User.objects.filter(username__regex=r'^.*{}.*$'.format(keyword))
#         users = User.objects.filter(username__icontains = keyword)
#         users_list = list(users.values_list('id', 'username'))    
#         return JsonResponse({'users': users_list})

# class ProjectController:
#     def index(request):
#         project_list = ProjectModel.objects.all()
#         paginator = Paginator(project_list, 3) # Show 25 contacts per page

#         page = request.GET.get('page')
#         projects = paginator.get_page(page)
#         return render(request, 'tool/project/index.html', {'projects': projects})

#     def create(request):
#         if request.method == "POST":
#             form = ProjectCreationForm(request.POST)
#             args = {'form': form}                     
#             if form.is_valid():
#                 new_project = form.save()
#                 members_data = request.POST.get('members')
#                 print(members_data)
#                 if(members_data != '' and members_data is not None):
#                     members = json.loads(members_data)
#                     ProjectMember.add_member_list(new_project, request.user, members) 
#                 return redirect(reverse('tool:project_edit', args=(new_project.id,)))
#             else:
#                 args['errors'] = form.errors
#                 return render(request, 'tool/project/create.html', args)
#         else: 
#             form = ProjectCreationForm(initial={'owner': request.user})
#             args = {'form': form}
#             return render(request, 'tool/project/create.html', args)
    
#     def view(request, id):
#         project = get_or_none(ProjectModel, pk=id)
#         if project is None:
#             return redirect('tool:page_not_found')
#         args = {'project': project}
#         return render(request, 'tool/project/view.html', args)

#     def edit(request, id):
#         project = ProjectModel.objects.get(id=id)
#         # check has permission edit project
#         is_owner_or_admin_or_supperuser = False or request.user.is_superuser
#         group_access = ProjectMember.get_group_access(request.user.id, project.id)
#         if(group_access == GroupAccess.OWNER or group_access == GroupAccess.ADMIN):
#             is_owner_or_admin_or_supperuser = True

#         if not is_owner_or_admin_or_supperuser:
#             return redirect('tool:error_no_access')

#         if request.method == "POST":
#             form = ProjectEditForm(request.POST,instance=project)
#             args = {'form': form}
#             if form.is_valid():
#                 form.save()
#                 # if(request.POST.get('members') != ''):
#                 #     member_list = json.loads(request.POST.get('members'))
#                 #     ProjectMember.update_project_member(project, request.user.id, member_list)                             
#                 members = ProjectMember.get_member_list(project)
#                 args['members'] = members                    
#                 return render(request, 'tool/project/edit.html', args)
#             else:
#                 print(ProjectMember.get_group_access(request.user.id, project_id))
#                 args['errors'] = form.errors
#                 return render(request, 'tool/project/edit.html', args)
#         else: 
#             project = ProjectModel.objects.get(id=id)
#             form = ProjectEditForm(instance=project)
#             members = ProjectMember.get_member_list(project)
#             args = {'form': form, 'members': json.dumps(members)}
#             return render(request, 'tool/project/edit.html', args)

#     def delete(request, id):
#         is_admin = request.user.is_superuser
#         if not is_admin:
#             return redirect('tool:error_no_access')
#         project_remove = get_or_none(ProjectModel, pk=id)
#         if project_remove is None:
#             return redirect('tool:page_not_found')
#         print(project_remove)
#         project_remove.delete()
#         messages.success(request, 'Project deleted successfully.')
#         return redirect('tool:project_index')

#     def estimate(request):
#         projects = ProjectModel.get_projects_has_access(request.user.id)
#         return render(request, 'tool/project/estimate.html', {'projects': projects})

#     def ajax_upload_csv(request):
#         if request.method == 'POST':
#             file_input = request.FILES['file']
#             data = ProjectController.handle_uploaded_file(file_input)
#             return JsonResponse({'data': data})

#     def ajax_add_project_memger(request):
#         if request.method == 'GET':
#             project_id = request.GET.get('project_id')
#             user_id = request.GET.get('user_id')
#             group_access = request.GET.get('group_access')
#             add_status = ProjectMember.add_project_member(request.user, project_id, user_id, group_access)
#             if add_status == -1:
#                 return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
#             elif add_status == -2:
#                 return JsonResponse({'status': 404, 'err': "Project member or Project not found"})
#             elif add_status == -3:
#                 return JsonResponse({'status': 500, 'err': "Member already added as project member"})
#             else:
#                 return JsonResponse({'status': 200, 'id': add_status})
#         else:
#             return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

#     def ajax_remove_project_member(request):
#         if request.method == 'GET':
#             project_id = request.GET.get('project_id')
#             project_member_id = request.GET.get('project_member_id')
#             remove_status = ProjectMember.remove_project_member(request.user, project_id, project_member_id)
#             if remove_status == -1:
#                 return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
#             elif remove_status == -2:
#                 return JsonResponse({'status': 404, 'err': "Project member not found"})
#             else:
#                 return JsonResponse({'status': 200})
#         else:
#             return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

#     def ajax_update_group_access(request):
#         if request.method == 'GET':
#             project_id = request.GET.get('project_id')
#             project_member_id = request.GET.get('project_member_id')
#             group_access = request.GET.get('group_access')
#             update_status = ProjectMember.update_group_access(request.user, project_member_id, group_access)
#             if update_status == -1:
#                 return JsonResponse({'status': 500, 'err': "You don't have access to do this action"})
#             elif update_status == -2:
#                 return JsonResponse({'status': 404, 'err': "Project member not found"})
#             else:
#                 return JsonResponse({'status': 200})
#         else:
#             return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

#     def ajax_get_project_detail(request):
#         if request.method == 'GET':
#             project_id = request.GET.get('project_id')
#             project = get_or_none(Project, pk=project_id)
#             if project is None:
#                 return JsonResponse({'status': 404, 'err': "Project not found"})
#             data = {}
#             data["pd"] = project.pd
#             data["budget"] = project.budget
#             data["status"] = project.status
#             return JsonResponse({'status': 200, 'data': data})
#         else:
#             return JsonResponse({'status': 500, 'err': 'Oops. Something wrong'})

#     def handle_uploaded_file(f):
#         workbook = xlrd.open_workbook(file_contents=f.read())
#         sheet = workbook.sheet_by_index(0)
#         nrows = sheet.nrows - 1
#         ncols = sheet.ncols
#         data = []
#         for col in range(sheet.ncols):
#             data.append(sheet.col_values(col))
#         for i in range(len(data)):
#             data[i].remove(data[i][0])
#         return data
            