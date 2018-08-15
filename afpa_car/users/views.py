from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import (PasswordResetView as BasePasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordResetCompleteView )
from django.core.mail import EmailMessage                                        
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url, urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm, LogoutForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .tokens import account_activation_token

User = get_user_model()

class SignUpView(TemplateView):
    template_name = 'users/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form,})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.private_data.afpa_number = form.cleaned_data["afpa_number"]
            user.private_data.phone_number = form.cleaned_data["phone_number"]
            user.private_data.save()

            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email =  form.cleaned_data["email"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'users/activation_link_send.html')

        return render(request, self.template_name, {'form': form,})

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            return render(request, 'users/activation.html')

        else:
            return render(request, 'users/activation.html',)

# class SignUpView(CreateView):
#     template_name = "users/signup.html"
#     success_url = reverse_lazy("carpooling:index")
#     form_class = SignupForm

#     def form_valid(self, form):
#         user = form.save()
#         user.private_data.afpa_number = form.cleaned_data["afpa_number"]
#         user.private_data.phone_number = form.cleaned_data["phone_number"]
#         user.private_data.save()
#         return super().form_valid(form)
    

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