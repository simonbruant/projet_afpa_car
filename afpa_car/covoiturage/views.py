from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, FormView, CreateView, DeleteView

from .forms import CarOwnerForm, AddressForm

from users.models import PrivateData, User
from .models import Address_User, Address

# TODO toutes les view requieres LoginRequiredMixin 

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

class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'covoiturage/profil/adresse.html'
    success_url = reverse_lazy('covoiturage:address') #TODO : changer index par la bonne page
    success_message = "Informations mises à jour"
    form_class = AddressForm

    # Lie User avec adresse lors de la creation de celle-ci
    def form_valid(self, form):
        user = self.request.user
        address = form.save()
        address_user = Address_User()
        address_user.address = address
        address_user.user = user
        address_user.save()
        return super(AddressCreateView, self).form_valid(form)

    # "Code a garder pour l'instant" - Amine
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     print ("# user ", user)
    #     return context

class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    fields = ('address_label', 'street_number', 'street_name', 'street_complement', 'zip_code', 'city')
    template_name = 'covoiturage/profil/adresse.html'
    success_url = reverse_lazy('covoiturage:address')
    success_message = "Informations mises à jour"
    form_class = AddressForm

    def get_object(self, queryset=None):
        user = Address.objects.get(user=self.request.user)
        return user

    def get_success_url(self):
        return reverse('covoiturage:address')


class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView ):
    model = Address
    success_url = reverse_lazy('covoiturage:address')


# class PrivateDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = PrivateData
#     fields = ('phone_number', 'afpa_number')
#     template_name = 'covoiturage/profil/infos_privees.html'
#     success_url = reverse_lazy('covoiturage:infos_privees')
#     success_message = "Informations mises à jour"

        
#     def get_object(self, queryset=None):
#         user = PrivateData.objects.get(user=self.request.user)
#         return user