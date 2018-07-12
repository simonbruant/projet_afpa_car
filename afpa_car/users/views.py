from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, SignupForm

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = '/reussi/'


class LoginView(FormView):
    form_class  = LoginForm
    success_url = '/reussi/'
    template_name = 'users/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('users:reussi')
        print("pas valide")
        return super(LoginView, self).form_invalid(form)
