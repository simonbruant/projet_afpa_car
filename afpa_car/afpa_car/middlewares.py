import re

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
if hasattr(settings, 'GLOBAL_URLS'):
    GLOBAL_URLS = [re.compile(url) for url in settings.GLOBAL_URLS]


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print('path :',path)
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        url_is_global = any(url.match(path) for url in GLOBAL_URLS)
        # print('authentic :', request.user.is_authenticated)
        # print("exempt :", url_is_exempt)
        # print("global :", url_is_global)
        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt or url_is_global:
            return None
        else:
            return redirect(settings.LOGIN_URL)