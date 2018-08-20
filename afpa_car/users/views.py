import datetime

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import (PasswordResetView as BasePasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordResetCompleteView )
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

User = get_user_model()

class HomeView(View):
    template_name = 'users/home.html'
    subject_template_name = 'users/activation_email_subject.txt'
    email_template_name = 'users/activation_email.html'
    from_email = None
    extra_email_context = None
    token_generator = account_activation_token


    def get(self, request):
        context = {
            'signup_form': SignupForm(),
            'login_form': LoginForm(),
        }
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        if 'login' in request.POST:
            print("login")
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                request = self.request
                next_ = request.GET.get('next')
                redirect_path = next_ or None
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data.get('password')
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

            context = {
                'login_form': login_form,
                'signup_form': SignupForm(),
            }

        elif 'signup' in request.POST:
            print("signup")

            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                user.is_active = False
                user.save()
                user.private_data.afpa_number = signup_form.cleaned_data["afpa_number"]
                user.private_data.phone_number = signup_form.cleaned_data["phone_number"]
                user.private_data.save()
                print(user)

                current_site = get_current_site(self.request)
                site_name = current_site.name
                domain = current_site.domain
                uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
                token = self.token_generator.make_token(user)
                use_https = request.is_secure()

                email_context = {
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
                    subject_template, email_template, email_context, from_email,
                    email,
                )
                return render(self.request, 'users/activation_link_send.html')

            context = {
                'login_form': LoginForm(),
                'signup_form': signup_form,
            } 
        return render(request, self.template_name, context)

    def send_mail(self, subject_template_name, email_template_name,
                context, from_email, to_email):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.send()

class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = SignupForm
    subject_template_name = 'users/activation_email_subject.txt'
    email_template_name = 'users/activation_email.html'
    from_email = None
    token_generator = account_activation_token

    def send_mail(self, subject_template_name, email_template_name,
                    context, from_email, to_email):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.send()

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        user.private_data.afpa_number = form.cleaned_data["afpa_number"]
        user.private_data.phone_number = form.cleaned_data["phone_number"]
        user.private_data.save()    

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

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print('user pk:', user.pk, user)
        print('token: ', account_activation_token.check_token(user, token))
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.confirm = True
            user.confirmation_date = timezone.now()
            user.save()
            return render(request, 'users/activation.html')
        else:
            return render(request, 'users/activation_link_invalid.html',)

class LoginView(FormView):
    form_class  = LoginForm
    template_name = 'carpooling/index.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        redirect_path = next_ or None
        email = form.cleaned_data['email']
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
        return render(request, self.template_name, {'form': form })

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