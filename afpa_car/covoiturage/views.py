from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView

from .forms import PrivateDataUpdateForm, UserUpdateForm, CarForm
from users.models import PrivateData, User
from covoiturage.models import Car, Car_User


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


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = 'covoiturage/profil/infos_publiques.html'
    success_url = reverse_lazy('covoiturage:infos_publiques')
    success_message = "Informations mises à jour"
    form_class = UserUpdateForm
    print('okkkk')
    
    def get_object(self, queryset=None):
        return self.request.user 

class CarCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):

    template_name = 'covoiturage/profil/vehicule.html'
    success_url = reverse_lazy('covoiturage:vehicule')
    success_message = "Informations mises à jour"
    form_class = CarForm
    print('jeazdjezd')

    def get_context_data(self, **kwargs):
        context = super(CarCreateView, self).get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(users=self.request.user)
        # context['car_owner'] = 
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
    success_url = reverse_lazy('covoiturage:vehicule_update')
    success_message = "Informations mises à jour"
    form_class = CarForm

    # def get_context_data(self, **kwargs):
    #     context = super(CarCreateView, self).get_context_data(**kwargs)
    #     context['cars'] = Car.objects.filter(users=self.request.user)
    #     return context
    


