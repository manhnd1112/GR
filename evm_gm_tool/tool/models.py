from django.db import models
from django.contrib.auth.models import User as AdminUser
from django.db.models.signals import post_save
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



class UserProfile(models.Model):
    user = models.OneToOneField(AdminUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])    
        
post_save.connect(create_profile, sender=AdminUser)