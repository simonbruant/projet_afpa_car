from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView, PasswordResetCompleteView )
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm, LogoutForm, PrivateDataCreateForm, PasswordChangeForm

class SignUpView(TemplateView):
    template_name = 'users/signup.html'

    def get(self, request):
        signup_form = SignupForm()
        private_data_form = PrivateDataCreateForm()

        context = {'signup_form': signup_form, 'private_data_form': private_data_form,}
        return render(request, self.template_name, context)

    def post(self, request):
        signup_form = SignupForm(request.POST)
        private_data_form = PrivateDataCreateForm(request.POST)
        if signup_form.is_valid() and private_data_form.is_valid():
            user = signup_form.save()
            private_data = private_data_form.save(commit=False)
            private_data.user = user
            private_data.save()
            return redirect("carpooling:index")

        context = {'signup_form': signup_form, 'private_data_form': private_data_form,}
        return render(request, self.template_name, context)

class LoginView(FormView):
    form_class  = LoginForm
    template_name = 'carpooling/index.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        redirect_path = next_ or None
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
                return redirect('carpooling:dashboard')
        return super(LoginView, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('carpooling:dashboard')
        else:
            form = self.form_class() 
            return render(request, self.template_name, {'form': form})

class LogoutView(LoginRequiredMixin, FormView):
    form_class = LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('carpooling:index'))

class ChangePassword(TemplateView):
    template_name = 'carpooling/profil/password.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        context = {'form': form }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('carpooling:dashboard')
        context = {'form': form }
        return render(request, self.template_name, context)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')