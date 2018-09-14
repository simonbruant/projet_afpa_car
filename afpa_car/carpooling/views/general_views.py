from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from afpa_car.mixins import SendMailMixin
from carpooling.forms import ContactForm

settings.app_static_url = 'carpooling/app'

class DashboardView(TemplateView):
    template_name = 'carpooling/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context = {
            'cars': user.cars.all(),
            'addresses': user.addresses.all(),
            'trips': user.default_trips.all(),
        }
        return context

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

