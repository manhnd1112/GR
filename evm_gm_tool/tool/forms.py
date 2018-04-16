from .models import User, Project, ProjectMember
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
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

class ProjectCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate form-control'}
    ))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control'
        }
    ))
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
    ))


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
    ))
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
    ))


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