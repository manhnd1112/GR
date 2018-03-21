from django.contrib import admin

# Register your models here.
from .models import Office, User, Project, ProjectMember, UserProfile

# admin.site.register(Office)
# admin.site.register(User)
# admin.site.register(Project)
# admin.site.register(ProjectMember)
admin.site.register(UserProfile)