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

class UserController:
    def index(request):
        user_list = User.objects.all()
        paginator = Paginator(user_list, 3) # Show 25 contacts per page

        page = request.GET.get('page')
        users = paginator.get_page(page)
        return render(request, 'tool/user/index.html', {'users': users})

    def create(request):
        is_admin = request.user.is_superuser
        if not is_admin:
            return redirect('tool:error_no_access')

        if request.method == "POST":
            form = UserCreateForm(request.POST)
            args = {'form': form}    
            if form.is_valid():
                new_user = form.save()
                return redirect(reverse('tool:user_edit', args=(new_user.id,)))
            else:
                args['errors'] = form.errors
                return render(request, 'tool/user/create.html', args)
        else: 
            form = UserCreateForm()
            args = {'form': form}
            return render(request, 'tool/user/create.html', args)

    def edit(request, id):
        is_admin = request.user.is_superuser
        if not is_admin:
            return redirect('tool:error_no_access')
        user_edit = get_or_none(User, pk=id)
        if user_edit is None:
            return redirect('tool:page_not_found')
        if request.method == "POST":
            form = UserEditForm(request.POST, instance=user_edit)                
            if form.is_valid():
                user_edit = form.save()                  
                return redirect(reverse('tool:user_edit', args=(user_edit.id,)))
            else:
                args = {'errors': form.errors, 'form': form}
                return render(request, 'tool/user/edit.html', args)
        else: 
            form = UserEditForm(instance=user_edit)
            args = {'form': form}
            return render(request, 'tool/user/edit.html', args)

    def delete(request, id):
        is_admin = request.user.is_superuser
        if not is_admin:
            return redirect('tool:error_no_access')
        user_remove = get_or_none(User, pk=id)
        if user_remove is None:
            return redirect('tool:page_not_found')
        user_remove.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('tool:user_index')

    # def ajax_search(request):
    #     keyword = request.GET.get('keyword')
    #     print(keyword)
    #     # users = User.objects.filter(username__regex=r'^.*{}.*$'.format(keyword))
    #     users = User.objects.filter(username__icontains = keyword)
    #     users_list = list(users.values_list('id', 'username'))    
    #     return JsonResponse({'users': users_list})
