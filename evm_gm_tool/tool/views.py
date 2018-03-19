from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Dashboard:
    template_name = 'evm_gm_tool/dashboard/index.html' 

    def index(request):
        return render(request, 'evm_gm_tool/dashboard/index.html' )