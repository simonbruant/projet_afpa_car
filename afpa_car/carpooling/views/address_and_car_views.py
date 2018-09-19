from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from carpooling.forms import AddressForm, CarForm
from carpooling.mixins import AddressMixin
from carpooling.models import Address, Car

settings.app_static_url = 'carpooling/app'
###### Car

class CarCreateView(SuccessMessageMixin, CreateView):
    template_name = 'carpooling/profil/car.html'
    success_url = reverse_lazy('carpooling:car')
    success_message = "Vehicule crée"
    form_class = CarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = self.request.user.cars.all()
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        return context


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
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        return context

##### Address

class AddressCreateView(AddressMixin, FormView):
    template_name = 'carpooling/profil/address.html'
    success_url = reverse_lazy('carpooling:address')
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['addresses'] = self.request.user.addresses.all()
        context['addresses_count'] = len(self.request.user.addresses.all())
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_view'] = True
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
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
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        return context

class AddressPOC(View):
    template_name = "carpooling/addr_poc.html"
    def get(self, request):
        context = {'address_poc_url': '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_ADDR_POC_FILE)}
        return render(request, self.template_name, context)