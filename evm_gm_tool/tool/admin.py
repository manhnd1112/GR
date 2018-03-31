from django.contrib import admin

# Register your models here.
from .models import UserProfile, Project, ProjectMember

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectMember)