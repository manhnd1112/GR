from django.db import models
from enum import IntEnum
from django.contrib.auth.models import User
from .utilies import *
import json
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    # members = models.ManyToManyField(Person, through='Membership')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile_image", blank=True)
    role = models.CharField(max_length=255, default='', blank=True)
    desc = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "user_profile"

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Project(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(default='', blank=True )
    status =  models.TextField(default='', blank=True) # save array of json objects: [{'AT': 1, 'PV': 10, 'EV': 7, 'AC':12}]
    budget = models.FloatField(default=0)
    pd = models.FloatField(default=0) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project"

    def get_ac(self):
        project_status = json.loads(self.status)
        if len(project_status) > 0:
            return project_status[len(project_status) - 1]["AC"]
        return 0

    def get_projects_has_access(user_id):
        user = get_or_none(User, pk = user_id)
        if user is None:
            return None
        projects = []
        if user.is_superuser:
            for project in Project.objects.all():
                projects.append(project)
            return projects
        projects_as_onwer = Project.objects.filter(owner=user)
        project_members = ProjectMember.objects.filter(user=user)
        for project in projects_as_onwer:
            projects.append(project)
        
        for project_member in project_members:
            projects.append(project_member.project)
        return projects

    def get_group_access(user_id, project_id):
        project = get_or_none(Project, pk=project_id)
        user = get_or_none(User, pk=user_id)
        if project is None or user is None:
            return -1
        if user.is_superuser:
            return GroupAccess.SUPERUSER
        if user == project.owner:
            return GroupAccess.OWNER
        try:
            project_member = ProjectMember.objects.get(project_id=project_id, user_id=user_id)
            return project_member.access
        except ProjectMember.DoesNotExist:
            return -1
    

            
class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.IntegerField() # ADMIN (full access), WRITE, READ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "project_member"

    def get_group_access(user_id, project_id):
        project = get_or_none(Project, pk=project_id)
        user = get_or_none(User, pk=user_id)
        if project is None or user is None:
            return -1
        if user.is_superuser:
            return GroupAccess.SUPERUSER
        if user == project.owner:
            return GroupAccess.OWNER
        try:
            project_member = ProjectMember.objects.get(project_id=project_id, user_id=user_id)
            return project_member.access
        except ProjectMember.DoesNotExist:
            return -1

    def add_member_list(project, user_create, member_list):
        group_access = ProjectMember.get_group_access(user_create.id, project.id)
        if group_access != GroupAccess.SUPERUSER and group_access != GroupAccess.OWNER and group_access != GroupAccess.ADMIN:
            return -1 # don't have access to update members
        for member in member_list:
            member_user = User.objects.get(pk=member["user-id"])
            project_member = get_or_none(ProjectMember, project=project, user=member_user)
            if project_member is None:
                new_project_member = ProjectMember(project=project, user=member_user, access=member["group-access"])
                new_project_member.save(True)
        return 0 # update success

    def remove_project_member(user_create, project_id, project_member_id):
        remove_project_member = get_or_none(ProjectMember, pk=project_member_id)
        if remove_project_member is None:
            return -2 # project member do not exits
        group_access = ProjectMember.get_group_access(user_create.id, remove_project_member.project.id)
        if group_access == -1 or group_access == GroupAccess.READ or group_access == GroupAccess.WRITE:
            return -1 # don't have access to update members
        remove_project_member.delete()
        return 0 # delete success

    def update_group_access(user_create, project_member_id, new_group_access):
        project_member = get_or_none(ProjectMember, pk=project_member_id)
        if project_member is None:
            return -2 # project member do not exits
        group_access = ProjectMember.get_group_access(user_create.id, project_member.project.id)
        if group_access == -1 or group_access == GroupAccess.READ or group_access == GroupAccess.WRITE:
            return -1 # don't have access to update members
        project_member.access = new_group_access
        project_member.save()
        return 0 # delete success

    def add_project_member(user_create, project_id, user_id, access):
        project = get_or_none(Project, pk=project_id)
        if project is None:
            return -2 # project not exits
        group_access = ProjectMember.get_group_access(user_create.id, project_id)
        if group_access == -1 or group_access == GroupAccess.READ or group_access == GroupAccess.WRITE:
            return -1 # don't have access to update members
        user = get_or_none(User, pk=user_id)
        if user is None:
            return -2 # user id not exits
        if get_or_none(ProjectMember, project = project, user=user) is None:
            new_project_member = ProjectMember(project=project, user=user, access=access)
            new_project_member.save(True)
            return new_project_member.id
        else:
            return -3 #project member already added

    def get_member_list(project):
        members_qs = ProjectMember.objects.filter(project=project)
        members = []
        member_index = 0
        for member_q in members_qs:
            member = {}
            member["id"] = member_q.id
            member["project_id"] = member_q.project.id 
            member["user_id"] = member_q.user.id 
            member["username"] = member_q.user.username 
            member["group_access"] = member_q.access 
            members.append(member)
        return members        

class GroupAccess(IntEnum):
    READ = 0
    WRITE = 1
    ADMIN = 2
    OWNER = 3
    SUPERUSER = 4