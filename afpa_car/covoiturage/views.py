from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, FormView

from .forms import CarOwnerForm
from users.models import PrivateData, User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'


class PrivateDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PrivateData
    fields = ('phone_number', 'afpa_number')
    template_name = 'covoiturage/profil/infos_privees.html'
    success_url = reverse_lazy('covoiturage:infos_privees')
    success_message = "Informations mises à jour"

    def get_object(self, queryset=None):
        user = PrivateData.objects.get(user=self.request.user)
        return user
        
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/calendar.html'

class CarOwnerView(UpdateView):
    model = User
    form_class = CarOwnerForm
    template_name = 'covoiturage/profil/vehicule.html'
    success_url = reverse_lazy('covoiturage:vehicule')

    def get_object(self, queryset=None):
        return self.request.user