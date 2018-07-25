from django.urls import path
from django.views.generic import TemplateView

from .views import DashboardView, AddressView
from users.views import LoginView, SignupView, LogoutView

app_name = 'covoiturage'

urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil.html")),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('profil/', AddressView.as_view(), name='profil'),
    path('test/', AddressView.as_view(), name='test'),
    # path('profil/adresse/', AdresseCreateView.as_view(), name='adresse'),
]