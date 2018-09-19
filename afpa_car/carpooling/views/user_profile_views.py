from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from carpooling.forms import ( PreferencesForm, PrivateDataUpdateForm, 
                    ProfilImageUpdateForm, UserProfileUpdateForm, UserUpdateForm)

settings.app_static_url = 'carpooling/app'

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
            'cars': user.cars.all(),
            'profil_url' : '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE),
            'general_infos_url' : '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_GENERAL_INFOS_FILE),
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        return context


class ProfilImageUpdateView(UpdateView):
    template_name = 'carpooling/profil/photo.html'
    success_url = reverse_lazy('carpooling:photo')
    form_class = ProfilImageUpdateForm

    def get_object(self, queryset=None):
        user_profile = self.request.user.user_profile
        return user_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temp = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        print( temp, "/////////////////////" )
        context['first_connection_url'] = temp
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        context['avatar_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_AVATAR_FILE)
        return context


class PreferencesUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'carpooling/profil/preferences.html'
    success_url = reverse_lazy('carpooling:preferences')
    success_message = "Préférences mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        user_profile = self.request.user.user_profile
        return user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PROFIL_FILE)
        context['preferences_url'] = '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_PREFERENCES_FILE)
        return context