from .models import User, Project, ProjectMember, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'validate',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Password'
        }
    ))

class UserCreateForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'validate form-control'}
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ), label='Password')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ), label='Password Confirmation')

    class Meta:
        model = User
        fields = (
            'email', 
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_superuser',
            'is_active'
        )

        labels = {
            'is_superuser': 'Is Admin',
        }
        #exclude = () 

class UserEditForm(UserChangeForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'validate form-control'}
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    class Meta:
        model = User
        fields = (
            'email', 
            'username',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'password'
        )

        labels = {
            'is_superuser': 'Is Admin',
        }

class ProjectCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate form-control'}
    ))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control'
        }
    ), required=False, label="Description")
    budget = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'step': 'any'
        }
    ))
    pd = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'step': 'any'
        }
    ), label="Project Duration")


    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'desc',
            'status',
            'budget',
            'pd',
            'owner'
        )

        labels = {
            'desc': 'Description'
        }

class ProjectEditForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
        }
    ))
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate form-control'}
    ))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control'
        }
    ), required=False, label="Description")
    budget = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'step': 'any'
        }
    ))
    pd = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'step': 'any'
        }
    ), label="Planned Duration")


    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'desc',
            'status',
            'budget',
            'pd',
            'owner'
        )

        labels = {
            'desc': 'Description'
        }

class ProjectViewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'desc',
            'status',
            'budget',
            'pd',
            'owner'
        )

        labels = {
            'desc': 'Description',
            'pd': 'Project Duration'
        }

class EditProfileForm(forms.ModelForm):
    role = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control role'
        }
    ), required=False, label='Work as')
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control desc'
        }
    ), required=False, label='Bio')
    class Meta:
        model = UserProfile

        fields = (
            'avatar',
            'role',            
            'desc'
        )

        labels = {
            'role': 'Work as'
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        } 
    ), label="Old password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        } 
    ), label="New password")

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        } 
    ), label="New password confirmation")