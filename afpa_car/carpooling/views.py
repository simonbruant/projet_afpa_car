from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

from .forms import PrivateDataUpdateForm, UserUpdateForm, CarForm, ProfilImageUpdateForm, PreferencesForm, UserProfileUpdateForm, AddressForm
from .models import Car, Car_User, Address
from users.models import PrivateData, User, UserProfile

class DashboardView(TemplateView):
    template_name = 'carpooling/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(users=self.request.user)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        
        return context

class CalendarView(TemplateView):
    template_name = 'carpooling/calendar.html'

class UserUpdateView(SuccessMessageMixin, TemplateView):
    template_name = 'carpooling/profil/general_infos.html'
    success_message = "Informations mises à jour"

    def get(self, request):
        user = request.user
        user_form = UserUpdateForm(instance=user)
        user_profile_form = UserProfileUpdateForm(instance=user.user_profile)
        
        context = {'user_form': user_form, 'user_profile_form': user_profile_form,}
        context['cars'] = Car.objects.filter(users=self.request.user)
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        user_form = UserUpdateForm(request.POST, instance=user)
        user_profile_form = UserProfileUpdateForm(request.POST, instance=user.user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect('carpooling:general_infos')

        context = {'user_form': user_form, 'user_profile_form': user_profile_form,}
        return render(request, self.template_name, context)

class PrivateDataUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'carpooling/profil/private_infos.html'
    success_url = reverse_lazy('carpooling:private_infos')
    success_message = "Informations mises à jour"
    form_class = PrivateDataUpdateForm
    
    def get_object(self, queryset=None):
        user = PrivateData.objects.get(user=self.request.user)       
        return user
        

class ProfilImageUpdateView(UpdateView):
    template_name = 'carpooling/profil/photo.html'
    success_url = reverse_lazy('carpooling:photo')
    form_class = ProfilImageUpdateForm
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user = UserProfile.objects.get(user=self.request.user)       
        return user
        
class PreferencesUpdateView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'carpooling/profil/preferences.html'
    success_url = reverse_lazy('carpooling:preferences')
    success_message = "Préférences mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        user_profile = UserProfile.objects.get(user=self.request.user)       
        return user_profile
        
class CarCreateView(SuccessMessageMixin, CreateView):
    template_name = 'carpooling/profil/car.html'
    success_url = reverse_lazy('carpooling:car')
    success_message = "Vehicule crée"
    form_class = CarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(users=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user
        car = form.save()
        
        car.model = form.cleaned_data['model'].capitalize()
        car_user = Car_User()
        car_user.car = car
        car_user.user = user
        car.save()
        car_user.save()
        return super(CarCreateView, self).form_valid(form)

class CarUpdateView(SuccessMessageMixin, UpdateView):
    model = Car
    template_name = 'carpooling/profil/car.html'
    success_message = "Informations du véhicule mises à jour"
    form_class = CarForm

    def get_success_url(self):
        return reverse('carpooling:car')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

class CarDeleteView(SuccessMessageMixin, DeleteView):
    model = Car
    template_name = 'carpooling/profil/car_delete.html'
    success_url = reverse_lazy('carpooling:car')


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
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
        context['addresses'] = Address.objects.filter(user=self.request.user)
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
