from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetView as BasePasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordResetCompleteView )
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm, LogoutForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class SignUpView(CreateView):
    template_name = "users/signup.html"
    success_url = reverse_lazy("carpooling:index")
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()
        user.private_data.afpa_number = form.cleaned_data["afpa_number"]
        user.private_data.phone_number = form.cleaned_data["phone_number"]
        user.private_data.save()
        return super().form_valid(form)

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

class ChangePassword(LoginRequiredMixin, TemplateView):
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


class PasswordResetView(BasePasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = PasswordResetForm

class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = SetPasswordForm