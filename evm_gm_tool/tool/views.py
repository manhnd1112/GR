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
            