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

class CommonController:  
    def upload_csv(request):
        if request.method == 'POST':
            file_input = request.FILES['file']
            data = CommonController.handle_uploaded_file(file_input)
            return JsonResponse({'data': data})

    def handle_uploaded_file(f):
        workbook = xlrd.open_workbook(file_contents=f.read())
        sheet = workbook.sheet_by_index(0)
        nrows = sheet.nrows - 1
        ncols = sheet.ncols
        data = []
        for col in range(sheet.ncols):
            data.append(sheet.col_values(col))
        for i in range(len(data)):
            data[i].remove(data[i][0])
        return data