from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, FormView

from .forms import (PrivateDataUpdateForm, UserUpdateForm, CarForm,
                    ProfilImageUpdateForm, PreferencesForm, UserProfileUpdateForm,
                    AddressForm, DefaultTripForm, DefaultTripFormSet, ContactForm)
from .models import Car, Address, DefaultTrip, AfpaCenter
from users.models import PrivateData, User, UserProfile

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

class UserUpdateView(SuccessMessageMixin, TemplateView):
    template_name = 'carpooling/profil/general_infos.html'
    success_message = "Informations mises à jour"

    def get(self, request):
        user = request.user
        user_form = UserUpdateForm(instance=user)
        user_profile_form = UserProfileUpdateForm(instance=user.user_profile)
        
        context = {
            'user_form': user_form, 
            'user_profile_form': user_profile_form,
            'cars': user.cars.all()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        user_form = UserUpdateForm(request.POST, instance=user)
        user_profile_form = UserProfileUpdateForm(request.POST, instance=user.user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile_form.save()
            return redirect('carpooling:general_infos')

        context = {
            'user_form': user_form, 
            'user_profile_form': user_profile_form,
            'cars': user.cars.all()
        }
        return render(request, self.template_name, context)

class PrivateDataUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'carpooling/profil/private_infos.html'
    success_url = reverse_lazy('carpooling:private_infos')
    success_message = "Informations mises à jour"
    form_class = PrivateDataUpdateForm
    
    def get_object(self, queryset=None):
        private_data = self.request.user.private_data      
        return private_data
        

class ProfilImageUpdateView(UpdateView):
    template_name = 'carpooling/profil/photo.html'
    success_url = reverse_lazy('carpooling:photo')
    form_class = ProfilImageUpdateForm

    def get_object(self, queryset=None):
        user_profile = self.request.user.user_profile       
        return user_profile
        
class PreferencesUpdateView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'carpooling/profil/preferences.html'
    success_url = reverse_lazy('carpooling:preferences')
    success_message = "Préférences mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        user_profile = self.request.user.user_profile       
        return user_profile
        
class CarCreateView(SuccessMessageMixin, CreateView):
    template_name = 'carpooling/profil/car.html'
    success_url = reverse_lazy('carpooling:car')
    success_message = "Vehicule crée"
    form_class = CarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = self.request.user.cars.all()
        return context

    def form_valid(self, form):
        user = self.request.user
        car = form.save(commit=False)
        car.model = form.cleaned_data['model'].capitalize()
        car.user = user
        car.save()
        return super().form_valid(form)

class CarUpdateView(SuccessMessageMixin, UpdateView):
    model = Car
    template_name = 'carpooling/profil/car.html'
    success_message = "Informations du véhicule mises à jour"
    form_class = CarForm

    def get_success_url(self):
        return reverse('carpooling:car')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class CarDeleteView(SuccessMessageMixin, DeleteView):
    model = Car
    template_name = 'carpooling/profil/car_delete.html'
    success_url = reverse_lazy('carpooling:car')


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = Car.objects.get(pk=self.kwargs['pk'])
        context['car'] = car
        return context


class AddressCreateView(SuccessMessageMixin, CreateView):
    template_name = 'carpooling/profil/address.html'
    success_url = reverse_lazy('carpooling:address')
    success_message = "Adresse crée"
    form_class = AddressForm

    def form_valid(self, form):
        address = form.save()
        address.user = self.request.user
        address_label = form.cleaned_data['address_label']
        address.address_label = "Adresse" if not address_label else address_label.capitalize()
        address.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['addresses'] = self.request.user.addresses.all()
        return context


class AddressUpdateView(SuccessMessageMixin, UpdateView):
    model = Address
    template_name = 'carpooling/profil/address.html'
    success_message = "Informations mises à jour"
    form_class = AddressForm

    def get_success_url(self):
        return reverse('carpooling:address')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        address = form.save()
        address_label = form.cleaned_data['address_label']
        address.address_label = "Adresse" if not address_label else address_label.capitalize()
        address.save()
        return super().form_valid(form)

class AddressDeleteView(SuccessMessageMixin, DeleteView):
    model = Address
    template_name = 'carpooling/profil/address_delete.html'
    success_url = reverse_lazy('carpooling:address')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.get(pk=self.kwargs['pk'])
        return context

class DefaultTripCreateView(SuccessMessageMixin, View):
    template_name = 'carpooling/calendar.html'
    success_message = "Mise à jour de la semaine type"

    def get(self, request):
        user=self.request.user
        formset = DefaultTripFormSet(queryset=DefaultTrip.objects.filter(user=user), form_kwargs={'user': user},)
        day_label = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        context = {
            'trips': user.default_trips.all(),
            'formset': formset,
            'day_label': day_label,
            'range': range(5),
            'form': DefaultTripForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = self.request.user
        formset = DefaultTripFormSet(request.POST, queryset=DefaultTrip.objects.filter(user=user), form_kwargs={'user': user})
        if formset.is_valid():
            print("formset is valid")
            x = 0
            for form in formset.forms:
                default_trip = form.save(commit=False)
                default_trip.user = user
                default_trip.has_for_destination = user.user_profile.afpa_center.address
                if not default_trip.day:
                    default_trip.day = default_trip._meta.get_field('day').choices[x][1]
                    x += 1
                default_trip.save()

            if self.success_message:
                messages.success(self.request, self.success_message)

            return redirect('carpooling:calendar')
        
        return render(request, self.template_name, {'formset': formset })

    def form_valid(self, form):
        print("form valid")
        default_trip = form.save(commit=False)
        default_trip.user = self.request.user
        return super().form_valid(form)

class ContactView(FormView):
    template_name = 'carpooling/contact.html'
    form_class = ContactForm    