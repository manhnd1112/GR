from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import Project as ProjectModel, ProjectMember, GroupAccess, UserProfile
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm, EditProfileForm, ChangePasswordForm
from tool.utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

class UserProfileController:
    def view(request, id):
        user = get_or_none(User, pk=id)
        if user is None:
            return redirect('tool:page_not_found')
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
        return render(request, 'tool/profile/view.html', {'profile': user.userprofile})

    def edit(request):
        user = request.user
        if user is None:
            return redirect('tool:page_not_found')
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
        if request.method == "POST":
            form = EditProfileForm(request.POST, request.FILES, instance=user.userprofile)                
            if form.is_valid():
                user.first_name = request.POST.get('firstname')
                user.last_name = request.POST.get('lastname')
                user.save()
                profile_edit = form.save()    
                messages.success(request, 'Profile updated successfully')              
                return redirect('tool:user_profile_edit')
            else:
                args = {'errors': form.errors, 'form': form, 'user': user}
                return render(request, 'tool/profile/edit.html', args)
        else:
            form = EditProfileForm(instance=user.userprofile)
            args = {'form': form}
            return render(request, 'tool/profile/edit.html', args)
    
    def change_password(request):
        if request.method == "POST":
            form = ChangePasswordForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully')                              
                return redirect('tool:user_profile_edit')
            else:
                return render(request, 'tool/profile/change_password.html',{'form': form})
        else:
            form = ChangePasswordForm(user=request.user)
            return render(request, 'tool/profile/change_password.html',{'form': form})            