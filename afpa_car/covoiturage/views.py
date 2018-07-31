from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

from .forms import CarOwnerForm, AddressForm
from .models import Address_User, Address
from users.models import PrivateData, User

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