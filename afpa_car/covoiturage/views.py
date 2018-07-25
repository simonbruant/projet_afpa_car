from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from .forms import * # TODO import selectif
from .models import Address_User, Address

# TODO toutes les view requieres LoginRequiredMixin 

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'

# Models adress
class AddressView(CreateView):
    form_class = AddressForm
    template_name = 'covoiturage/test.html'
    success_url = reverse_lazy('covoiturage:test')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     user = self.request.user
                
    #     print ("# user ", user)
    #     return context

    def form_valid(self, form):
        user = self.request.user
        address = form.save()
        
        address_user = Address_User()
        address_user.address = address
        address_user.user = user
        address_user.save()

        return super(AddressView, self).form_valid(form)