from django.urls import path
from . import views
from django.contrib.auth.views import login

app_name = 'tool'
urlpatterns = [
    path('', views.Dashboard.index, name="index"),
    path("login/", login, {'template_name': 'evm_gm_tool/auth/login.html'})
]