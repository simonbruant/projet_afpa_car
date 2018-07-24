from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import PrivateDataUpdateForm
from users.models import PrivateData


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'


class PrivateDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # model = PrivateData
    # fields = ('phone_number', 'afpa_number')
    template_name = 'covoiturage/profil/infos_privees.html'
    success_url = reverse_lazy('covoiturage:infos_privees')
    success_message = "Informations mises à jour"
    form_class = PrivateDataUpdateForm

    def get_object(self, queryset=None):
        user = PrivateData.objects.get(user=self.request.user)
        return user
        # return self.request.user #pour user