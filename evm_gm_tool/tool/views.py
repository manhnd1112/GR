from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from tool.forms import (
    RegistrationForm, 
    EditProfileForm
)

class Dashboard:
    template_name = 'evm_gm_tool/dashboard/index.html' 

    def index(request):
        return render(request, 'evm_gm_tool/dashboard/index.html' )
    
    def register(request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/tool')
        else:
            form = RegistrationForm()
            args = {'form': form}
            return render(request, 'evm_gm_tool/auth/reg_form.html', args)
    
    @login_required
    def view_profile(request):
        args = {'user': request.user}
        return render(request, 'evm_gm_tool/auth/profile.html', args)

    @login_required    
    def edit_profile(request):
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/tool/profile')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'evm_gm_tool/auth/edit_profile.html', args)
    
    @login_required    
    def change_password(request):
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/tool/profile')
            else:
                return redirect('/tool/change-password')
        else: 
            form = PasswordChangeForm(user=request.user)
            args = {'form': form}
            return render(request, 'evm_gm_tool/auth/change_password.html', args)