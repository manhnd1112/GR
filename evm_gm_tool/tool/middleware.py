import re
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import Http404

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
ADMIN_URLS = []
if hasattr(settings, 'LOGIN_EXEMPLT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPLT_URLS]

if hasattr(settings, 'ADMIN_URL'):
    ADMIN_URLS += [re.compile(settings.ADMIN_URL)]

class LoginRequireMiddleware:   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwagrs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(path)
        # if not request.user.is_authenticated:
        #     if not any(url.match(path) for url in EXEMPT_URLS):
        #         return redirect('tool:login')
        
        url_is_exempt =  any(url.match(path) for url in EXEMPT_URLS)
        url_is_admin = any(url.match(path) for url in ADMIN_URLS)
        if settings.LOGOUT_URL.match(path):
            logout(request)
            return None

        if url_is_admin:
            return redirect('tool:homepage')
        # if url_is_admin:
        #     return None
        elif request.user.is_authenticated and url_is_exempt:
            print('Redirect to homepage')
            return redirect('tool:homepage')
        elif request.user.is_authenticated and (not url_is_exempt):
            print('Force: Logged')  
            return None
        elif (not request.user.is_authenticated) and url_is_exempt:
            return None
        else:
            print('Redirect to login')            
            return redirect('tool:login')