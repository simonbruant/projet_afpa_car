from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate

from .forms import LoginForm, RegisterForm

# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = '/users/reussi/'
