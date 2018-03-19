from django.db import models

# Create your models here.

class Office(models.Model):
    name = models.CharField(max_length=255, unique=True)
    desc = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "office"

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)    
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255) 
    lastname = models.CharField(max_length=255) 
    avatar_url = models.CharField(max_length=255)
    desc = models.TextField()
    is_admin = models.BooleanField(default=False)
    office_id = models.ForeignKey(Office, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "user"

class Project(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    status =  models.TextField() # save array of json objects: [{'AT': 1, 'PV': 10, 'EV': 7, 'AC':12}]
    budget = models.FloatField()
    pd = models.FloatField() 
    created_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project"

class ProjectMember(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.IntegerField() # ADMIN (delete, write, add member), WRITE, READ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project_member"
