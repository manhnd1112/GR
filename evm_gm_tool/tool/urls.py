from django.urls import path
from . import views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tool'
urlpatterns = [
    path("", views.Dashboard.index, name="homepage"),   
    path("error/no_access", views.Dashboard.error_no_access, name="error_no_access"),   
    path("page_not_found", views.Dashboard.page_not_found, name="page_not_found"),   
    path("login/", login, {'template_name': 'evm_gm_tool/auth/login.html'}, name='login'),
    path("users/", views.UserController.index, name="user_index"),
    path("user/add/", views.UserController.create, name="user_add"),
    path("user/edit/<id>", views.UserController.edit, name="user_edit"),
    path("user/delete/<id>", views.UserController.delete, name="user_delete"),
    path("projects/", views.ProjectController.index, name="project_index"),
    path("project/create/", views.ProjectController.create, name="project_create"),
    path("project/view/<id>", views.ProjectController.view, name="project_view"),    
    path("project/edit/<id>", views.ProjectController.edit, name="project_edit"),
    path("project/delete/<id>", views.ProjectController.delete, name="project_delete"),
    path("estimate/", views.EstimateController.index, name="estimate_index"),
    path("estimate/estimate", views.EstimateController.estimate, name="estimate_estimate"),
    path("common/upload_csv", views.CommonController.upload_csv, name="common_upload_csv"),        
    path("ajax/search_user", views.AjaxController.search_user, name="ajax_search_user"),   
    path("ajax/add_project_member", views.AjaxController.add_project_memger, name="ajax_add_project_member"),
    path("ajax/update_group_access", views.AjaxController.update_group_access, name="ajax_update_group_access"),
    path("ajax/remove_member", views.AjaxController.remove_project_member, name="ajax_remove_member"),
    path("ajax/get_project_detail", views.AjaxController.get_project_detail, name="ajax_get_project_detail"),    
]