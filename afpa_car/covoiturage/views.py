from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import render, redirect
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
    form_class = AddressForm
    success_message = "Informations de création"

    # Lie User avec adresse lors de la creation de celle-ci
    def form_valid(self, form):
        user = self.request.user
        address = form.save()
        address_user = Address_User()

        address_user.address = address
        address_user.user = user
        address_user.save()

        print("mauvais comportement")
        return super(AddressCreateView, self).form_valid(form) #◘fonctionne avec super() vide

    # Déclare context de address afin de faire une boucle for pour en obtenir l'user lié
    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['address_context'] = Address.objects.filter(users=self.request.user)
        return context


class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    template_name = 'covoiturage/profil/adresse.html'
    success_message = "Informations mises à jour"
    form_class = AddressForm

    def get_success_url(self):
        print("bon comportement")
        return reverse('covoiturage:address')

    def get_queryset(self):
        queryset = super(AddressUpdateView, self).get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset


class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView ):
    model = Address
    template_name = 'covoiturage/profil/address_delete.html'
    success_url = reverse_lazy('covoiturage:address')