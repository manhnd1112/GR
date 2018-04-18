from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import Project as ProjectModel, ProjectMember, GroupAccess, UserProfile
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm, EditProfileForm
from tool.utilies import *
import xlrd, json
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class UserProfileController:
    def edit(request, id):
        if request.user.id != int(id):
            return redirect('tool:error_no_access')
        user = get_or_none(User, pk=id)
        if user is None:
            return redirect('tool:page_not_found')
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
        if request.method == "POST":
            print(request.FILES)
            form = EditProfileForm(request.POST, request.FILES, instance=user.userprofile)                
            if form.is_valid():
                profile_edit = form.save()                  
                return redirect(reverse('tool:user_profile_edit', args=(request.user.id,)))
            else:
                args = {'errors': form.errors, 'form': form}
                return render(request, 'tool/profile/edit.html', args)
        else:
            form = EditProfileForm(instance=user.userprofile)
            args = {'form': form}
            return render(request, 'tool/profile/edit.html', args)