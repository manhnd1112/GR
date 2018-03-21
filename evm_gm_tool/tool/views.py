from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

class Dashboard:
    template_name = 'evm_gm_tool/dashboard/index.html' 

    def index(request):
        return render(request, 'evm_gm_tool/dashboard/index.html' )
    
    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/tool')
        else:
            form = UserCreationForm()
            args = {'form': form}
            return render(request, 'evm_gm_tool/auth/reg_form.html', args)
