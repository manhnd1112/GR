from django.contrib import admin

# Register your models here.
from .models import Office, User, Project, ProjectMember

admin.site.register(Office)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectMember)