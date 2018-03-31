from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile_image", blank=True)
    desc = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "user_profile"

class Project(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(default='', blank=True)
    status =  models.TextField(default='', blank=True) # save array of json objects: [{'AT': 1, 'PV': 10, 'EV': 7, 'AC':12}]
    budget = models.FloatField(default=0)
    pd = models.FloatField(default=0) 
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project"

class ProjectMember(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.IntegerField() # ADMIN (full access), WRITE, READ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project_member"
