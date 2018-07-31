from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, RedirectView

from .forms import PrivateDataUpdateForm, UserUpdateForm, CarForm, FormationSessionForm, AfpaCenterForm, PreferencesForm, ProfilImageUpdateForm, AddressForm
from .models import Car, Car_User, Address_User, Address, FormationSession
from users.models import PrivateData, User

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'

class ProfilRedirectview(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('covoiturage:infos_publiques')

class PrivateDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'covoiturage/profil/infos_privees.html'
    success_url = reverse_lazy('covoiturage:infos_privees')
    success_message = "Informations mises à jour"
    form_class = PrivateDataUpdateForm
    
    def get_object(self, queryset=None):
        user = PrivateData.objects.get(user=self.request.user)       
        return user
        
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/calendar.html'

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = 'covoiturage/profil/infos_publiques.html'
    success_url = reverse_lazy('covoiturage:infos_publiques')
    success_message = "Informations mises à jour"
    form_class = UserUpdateForm
    
    def get_object(self, queryset=None):
        return self.request.user 

class CarCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    template_name = 'covoiturage/profil/vehicule.html'
    success_url = reverse_lazy('covoiturage:vehicule')
    success_message = "Informations mises à jour"
    form_class = CarForm

    def get_context_data(self, **kwargs):
        context = super(CarCreateView, self).get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(users=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user
        car = form.save()

        car_user = Car_User()
        car_user.car = car
        car_user.user = user
        car_user.save()
        return super(CarCreateView, self).form_valid(form)

class CarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Car
    template_name = 'covoiturage/profil/vehicule.html'
    success_message = "Informations mises à jour"
    form_class = CarForm

    def get_success_url(self):
        return reverse('covoiturage:vehicule')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

class CarDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Car
    template_name = 'covoiturage/profil/car_delete.html'
    success_url = reverse_lazy('covoiturage:vehicule')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

class ProfilImageUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'covoiturage/profil/photo.html'
    success_url = reverse_lazy('covoiturage:photo')
    form_class = ProfilImageUpdateForm
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

class PreferencesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'covoiturage/profil/preferences.html'
    success_url = reverse_lazy('covoiturage:preferences')
    success_message = "Informations mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        return self.request.user

class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'covoiturage/profil/adresse.html'
    success_url = reverse_lazy('covoiturage:address')
    success_message = "Informations de création"
    form_class = AddressForm

    def form_valid(self, form):
        user = self.request.user
        address = form.save()
        address_user = Address_User()
        street_number = form.cleaned_data['street_number']
        address.street_number = "" if not street_number else street_number

        address_user.address = address
        address_user.user = user
        address_label = form.cleaned_data['address_label']
        address_user.address_label_private = "Adresse" if not address_label else address_label
        address_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['address_user_context'] = Address_User.objects.filter(user=self.request.user)
        return context


class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    template_name = 'covoiturage/profil/adresse.html'
    success_message = "Informations mises à jour"
    form_class = AddressForm

    def get_success_url(self):
        return reverse('covoiturage:address')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

    def get_initial(self):
        address = Address.objects.get(pk=self.kwargs['pk'])
        address_user = Address_User.objects.get(user=self.request.user, address=address,)
        return {'address_label': address_user.address_label_private }
    
    def form_valid(self, form):
        address = form.save()
        street_number = form.cleaned_data['street_number']
        address.street_number = " " if not street_number else street_number
        address_label = form.cleaned_data['address_label']

        address_user = Address_User.objects.get(user=self.request.user, address=address,)
        address_user.address_label_private = address_user.address_label_private = "Adresse" if not address_label else address_label
        address_user.save()
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView ):
    model = Address
    template_name = 'covoiturage/profil/address_delete.html'
    success_url = reverse_lazy('covoiturage:address')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = Address.objects.get(pk=self.kwargs['pk'])
        context['address_context'] = address
        context['address_user_context'] = Address_User.objects.get(user=self.request.user, address=address,)
        return context
