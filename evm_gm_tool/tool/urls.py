from django.urls import path
from . import views
from django.contrib.auth.views import login, logout

app_name = 'tool'
urlpatterns = [
    path("", views.Dashboard.index, name="index"),    
    path("login/", login, {'template_name': 'evm_gm_tool/auth/login.html'}),
    path("logout/", logout, {'template_name': 'evm_gm_tool/auth/logout.html'}),
    path("register/", views.Dashboard.register, name='register'), 
    path("profile/", views.Dashboard.view_profile, name='view_profile'),    
    path("profile/edit/", views.Dashboard.edit_profile, name='edit_profile'),  
    path("change-password", views.Dashboard.change_password, name='change_password')    
]