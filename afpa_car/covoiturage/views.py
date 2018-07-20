from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from .forms import * # TODO import selectif

# TODO toutes les view requieres LoginRequiredMixin 

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'





# Models adress
class AddressView(CreateView):
    form_class = AddressForm
    template_name = 'covoiturage/test.html'
    success_url = reverse_lazy('covoiturage:index')

#     # AdressCreateForm / UpdateForm / DeleteForm