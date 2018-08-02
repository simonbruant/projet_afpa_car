from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, RedirectView, FormView
from django.views.generic.edit import FormMixin

from .forms import PrivateDataUpdateForm, UserUpdateForm, CarForm, ProfilImageUpdateForm, PreferencesForm#, UserProfileUpdateForm #, AddressForm
from .models import Car, Car_User, Address
from users.models import PrivateData, User, UserProfile

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'carpooling/dashboard.html'

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'carpooling/calendar.html'
    
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'carpooling/profil/general_infos.html'
    success_url = reverse_lazy('carpooling:general_infos')
    success_message = "Informations mises à jour"
    form_class = UserUpdateForm
    
    def get_object(self, queryset=None):
        return self.request.user 

    def get_initial(self):
        initials = {}
        user_profile = self.request.user.user_profile
        initials['afpa_center'] = user_profile.afpa_center.pk if user_profile.afpa_center else None
        initials['driver_license'] = user_profile.driver_license
        initials['car_owner'] = user_profile.car_owner
        initials['trainee'] = user_profile.trainee
        return initials

    def form_valid(self, form):
        user_profile = self.request.user.user_profile
        user_profile.afpa_center = form.cleaned_data['afpa_center']
        user_profile.driver_license = form.cleaned_data['driver_license']
        user_profile.car_owner = form.cleaned_data['car_owner']
        user_profile.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)



# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
#     template_name = 'carpooling/profil/general_infos.html'
#     success_message = "Informations mises à jour"

#     def get(self, request):
#         user = self.request.user
#         user_form = UserUpdateForm(
#             initial={
#                 'email': user.email,
#                 'username': user.username,
#                 'last_name': user.last_name,
#                 'first_name': user.first_name,
#             }
#         )
#         user_profile_form = UserProfileUpdateForm(
#             initial= {
#                 'afpa_center': user.user_profile.afpa_center,
#                 'trainee': user.user_profile.trainee,
#                 'driver_license': user.user_profile.driver_license,
#                 'car_owner': user.user_profile.car_owner,
#             }
#         )

#         context = {'user_form': user_form, 'user_profile_form': user_profile_form,}
#         return render(request, self.template_name, context)

#     def post(self, request):
#         user_form = UserUpdateForm(request.POST)
#         user_profile_form = UserProfileUpdateForm(request.POST)
#         print('ok 1')
#         print(user_form.is_valid(), user_profile_form.is_valid())
#         if user_form.is_valid() and user_profile_form.is_valid():
#             user = user_form.save()
#             print("1")
#             user_profile = user_profile_form.save(commit=True)
#             print("2")
#             user_profile.user = user
#             print("3")
#             user_profile.save()
#             print('form valid')
#             return redirect('carpooling:general_infos')
#         else:
#             print('else')

#         context = {'user_form': user_form, 'user_profile_form': user_profile_form,}
#         return render(request, self.template_name, context)


class PrivateDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'carpooling/profil/private_infos.html'
    success_url = reverse_lazy('carpooling:private_infos')
    success_message = "Informations mises à jour"
    form_class = PrivateDataUpdateForm
    
    def get_object(self, queryset=None):
        user = PrivateData.objects.get(user=self.request.user)       
        return user
        

class ProfilImageUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'carpooling/profil/photo.html'
    success_url = reverse_lazy('carpooling:photo')
    form_class = ProfilImageUpdateForm
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user = UserProfile.objects.get(user=self.request.user)       
        return user
        
class PreferencesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'carpooling/profil/preferences.html'
    success_url = reverse_lazy('carpooling:preferences')
    success_message = "Informations mises à jour"
    form_class = PreferencesForm

    def get_object(self, queryset=None):
        user_profile = UserProfile.objects.get(user=self.request.user)       
        return user_profile
        
class CarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'carpooling/profil/car.html'
    success_url = reverse_lazy('carpooling:car')
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
    template_name = 'carpooling/profil/car.html'
    success_message = "Informations mises à jour"
    form_class = CarForm

    def get_success_url(self):
        return reverse('carpooling:car')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

class CarDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
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


# class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     template_name = 'carpooling/profil/address.html'
#     success_url = reverse_lazy('carpooling:address')
#     success_message = "Adresse créee"
#     form_class = AddressForm

#     def form_valid(self, form):
#         address = form.save()
#         address_user = Address_User()

#         address_user.address = address
#         address_user.user = self.request.user
#         address_label = form.cleaned_data['address_label']
#         address_user.address_label_private = "Adresse" if not address_label else address_label
#         address_user.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(AddressCreateView, self).get_context_data(**kwargs)
#         context['address_user_context'] = Address_User.objects.filter(user=self.request.user)
#         return context


# class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Address
#     template_name = 'carpooling/profil/address.html'
#     success_message = "Informations mises à jour"
#     form_class = AddressForm

#     def get_success_url(self):
#         return reverse('carpooling:address')

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(users=self.request.user)
#         return queryset

#     def get_initial(self):
#         address = Address.objects.get(pk=self.kwargs['pk'])
#         address_user = Address_User.objects.get(user=self.request.user, address=address,)
#         return {'address_label': address_user.address_label_private }
    
#     def form_valid(self, form):
#         address = form.save()
#         address_label = form.cleaned_data['address_label']

#         address_user = Address_User.objects.get(user=self.request.user, address=address,)
#         address_user.address_label_private = address_user.address_label_private = "Adresse" if not address_label else address_label
#         address_user.save()
#         return super().form_valid(form)

# class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Address
#     template_name = 'carpooling/profil/address_delete.html'
#     success_url = reverse_lazy('carpooling:address')

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(users=self.request.user)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         address = Address.objects.get(pk=self.kwargs['pk'])
#         context['address_user_context'] = Address_User.objects.get(user=self.request.user, address=address,)
#         return context
