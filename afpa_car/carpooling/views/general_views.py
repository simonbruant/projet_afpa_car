from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, UpdateView

from afpa_car.mixins import SendMailMixin
from carpooling.forms import ContactForm, FirstConnectionForm

from users.models import UserProfile

settings.app_static_url = 'carpooling/app'

class DashboardView(UpdateView):
    model = UserProfile
    template_name = 'carpooling/dashboard.html'
    form_class = FirstConnectionForm
    success_url = reverse_lazy('carpooling:dashboard')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['cars'] = user.cars.all()
        context['addresses'] = user.addresses.all()
        context['trips'] = user.default_trips.all()
        context['proposition'] = user.second_user.all()
        context['user_first_connection'] = user.first_connection
        context['first_connection_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_FIRST_CONNECTION_FILE)
        return context

    def get_object(self, queryset=None):
        user_profile = self.request.user.user_profile
        return user_profile

    def form_valid(self, form ):
        print("valid ok")
        user = self.request.user
        user.first_connection = False
        user.save()
        form.save()
        return super().form_valid(form)

class ContactView(SendMailMixin, FormView):
    template_name = 'carpooling/contact.html'
    to_email = 'test@gmail.com'
    email_template_name = 'carpooling/contact_email.html'
    subject_template_name = 'carpooling/contact_email_subject.html'
    form_class = ContactForm
    success_url = reverse_lazy('carpooling:index')
    
    def get_initial(self):
        user = self.request.user
        initial = {}
        if user.is_authenticated:
            initial['name'] = user.get_full_name()
            initial['email'] = user.email
        return initial

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        from_email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')

        context = {
            'name': name,
            'date': timezone.now(),
            'subject': subject,
            "message": message,
        }

        to_email = self.to_email
        subject_template = self.subject_template_name
        email_template = self.email_template_name

        self.send_mail(
            subject_template, email_template, context, from_email,
            to_email,
        )
        return super().form_valid(form)

