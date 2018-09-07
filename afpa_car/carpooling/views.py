import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, ListView, DetailView, FormView

from .forms import (PrivateDataUpdateForm, UserUpdateForm, CarForm,
                    ProfilImageUpdateForm, PreferencesForm, UserProfileUpdateForm,
                    AddressForm, DefaultTripForm, DefaultTripFormSet, ContactForm)
from .mixins import AddressMixin
from .models import Car, Address, DefaultTrip, AfpaCenter, Trip
from afpa_car.mixins import SendMailMixin
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

class UserUpdateView(SuccessMessageMixin, View):
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
        user_profile_form = UserProfileUpdateForm(
            request.POST, instance=user.user_profile)
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


class AddressCreateView(AddressMixin, FormView):
    template_name = 'carpooling/profil/address.html'
    success_url = reverse_lazy('carpooling:address')
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['addresses'] = self.request.user.addresses.all()
        context['addresses_count'] = len(self.request.user.addresses.all())
        return context

class AddressUpdateView(AddressMixin, UpdateView):
    model = Address
    template_name = 'carpooling/profil/address.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse('carpooling:address')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['update_view'] = True
        return context


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


class DefaultTripView(SuccessMessageMixin, View):
    template_name = 'carpooling/calendar.html'
    success_message = "Mise à jour de la semaine type"

    def get(self, request):
        user = self.request.user
        formset = DefaultTripFormSet(queryset=DefaultTrip.objects.filter(
            user=user), form_kwargs={'user': user},)
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
        formset = DefaultTripFormSet(request.POST, queryset=DefaultTrip.objects.filter(user=user), 
                                    form_kwargs={'user': user})
        for i, form in enumerate(formset.forms):
            if form.is_valid():
                default_trip = form.save(commit=False)
                default_trip.user = user
                default_trip.has_for_destination = user.user_profile.afpa_center.address

                is_form_valid = (not form.cleaned_data.get('morning_departure_time') 
                                or not form.cleaned_data.get('morning_arriving_time')
                                or not form.cleaned_data.get('evening_departure_time')
                                or not form.cleaned_data.get('has_for_start')
                                or form.cleaned_data.get('deactivate'))

                if is_form_valid:
                    default_trip.has_for_start = None
                    default_trip.morning_departure_time = None
                    default_trip.morning_arriving_time = None
                    default_trip.evening_departure_time = None
                    default_trip.deactivate = True

                default_trip.day = default_trip._meta.get_field('day').choices[i][1]
                default_trip.save()

        if self.success_message:
            messages.success(self.request, self.success_message)

        return redirect('carpooling:calendar')
        
class TripView(View):
    template_name = 'carpooling/trip.html'

    def get(self, request):
        query = request.GET.get('query')
        query_day = request.GET.get('query_day')
        context = {}
        if not query and not query_day:
            context['trips'] = DefaultTrip.objects.all()
        else:
            trips = DefaultTrip.objects.filter(has_for_start__city__startswith=query,
                                                day__startswith=query_day)
            context['trips'] = trips
                                            # Q(day__startswith=query)
                                            # Q(user__first_name__icontains=query)
                                            # Q(day__startswith=query) | Q(user__first_name__icontains=query)

        return render(request, 'carpooling/trip.html', context)


class TripDetailView(DetailView):
    model = DefaultTrip
    template_name = 'carpooling/trip.html'

    def get(self, request, trip_id) :
        
        trip = get_object_or_404(DefaultTrip, pk=trip_id)
        user = request.user
        # print(Car.objects.filter(user)) 
        # Car.objects.all(self.request.user)
        # car = trip.user.cars.all()[0]
        context = {
            'trip' : trip,
            # 'trip_car': car,
            # 'trip_amount_of_free_seats': range(car.amount_of_free_seats),
        }
        return render(request, 'carpooling/trip_detail.html', context)

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

class PropositionView(TemplateView):
    template_name = 'carpooling/proposition.html'
