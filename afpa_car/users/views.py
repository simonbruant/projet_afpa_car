from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate

from .forms import LoginForm

# Create your views here.
class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'users/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = 