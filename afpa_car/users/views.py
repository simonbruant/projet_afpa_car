import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import (PasswordResetView as BasePasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordResetCompleteView, 
                                        LogoutView as BaseLogoutView)
from django.core.mail import EmailMessage, EmailMultiAlternatives                                        
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url, urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm, LogoutForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .tokens import account_activation_token
from afpa_car.mixins import SendMailMixin

User = get_user_model()

settings.app_static_url = 'carpooling/{}'.format('app')

class SignUpView(SendMailMixin, CreateView):
    template_name = "users/signup.html"
    form_class = SignupForm
    subject_template_name = 'users/activation_email_subject.txt'
    email_template_name = 'users/activation_email.html'
    from_email = None
    token_generator = account_activation_token

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        user.private_data.afpa_number = form.cleaned_data["afpa_number"]
        user.private_data.phone_number = form.cleaned_data["phone_number"]
        user.user_profile.afpa_center = form.cleaned_data["afpa_center"]
        user.private_data.save()    
        user.user_profile.save()    

        # Envoie email de confirmation
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = self.token_generator.make_token(user)
        use_https = self.request.is_secure()

        context = {
            'domain': domain,
            'site_name': site_name,
            'uid': uid,
            'token': token,
            'protocol': 'https' if use_https else 'http',
        }

        subject_template = self.subject_template_name
        email_template = self.email_template_name
        from_email = self.from_email
        email = user.email

        self.send_mail(
            subject_template, email_template, context, from_email,
            email,
        )

        return render(self.request, 'users/activation_link_send.html')

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.confirm = True
            user.confirmation_date = timezone.now()
            user.save()
            return render(request, 'users/activation.html')
        else:
            return render(request, 'users/activation_link_invalid.html',)

class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'carpooling/index.html'

class LogoutView(FormView):
    form_class = LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('carpooling:index'))

class ChangePassword(View):
    template_name = 'carpooling/profil/password.html'

    def get(self, request):
        print(settings.app_static_url, "CHANGE PASSWORD ##############################")
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form, 
            'profil_url': '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        }
        return render(request, self.template_name, context )


    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('carpooling:dashboard')
        return render(request, self.template_name, {'form': form })

class PasswordResetView(BasePasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = PasswordResetForm

class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = SetPasswordForm