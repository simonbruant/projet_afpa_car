from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView

from .forms import PrivateDataUpdateForm, UserUpdateForm, CarForm, FormationSessionForm, AfpaCenterForm, PreferencesForm
from .models import Car, Car_User, FormationSession
from users.models import PrivateData, User


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
        
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/calendar.html'

def email(request):
    send_mail('Hello', 
    'Hello',
    settings.EMAIL_HOST_USER,
    ['gaziya@loketa.com'],)

    return render(request, 'covoiturage/email.html')


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


@login_required(login_url='covoiturage:index')
def FormationSessionCreateView(request):
    formationSession_form = FormationSessionForm(request.POST or None)
    afpa_center_form = AfpaCenterForm(request.POST or None)

    if formationSession_form.is_valid() and afpa_center_form.is_valid():
        print('ok')
        formationSession_form.save()
        afpa_center_form.save()
        return redirect("covoiturage:formation") 

    return render(
        request, 
        'covoiturage/profil/formation.html', 
        {   'formationSession_form': formationSession_form,
            'afpa_center_form': afpa_center_form,}
    )

class PreferencesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'covoiturage/profil/preferences.html'
    success_url = reverse_lazy('covoiturage:preferences')
    success_message = "Informations mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        return self.request.user 






    


