from django.urls import path
from django.views.generic import TemplateView

from .views import DashboardView, PrivateDataUpdateView, CalendarView, CarOwnerView, AddressCreateView, AddressUpdateView, AddressDeleteView
from users.views import LoginView, LogoutView, signup_view, change_password

app_name = 'covoiturage'

urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil/infos_publiques.html"), name='profil'),
    path('profil/infos_publiques/', TemplateView.as_view(template_name="covoiturage/profil/infos_publiques.html"), name='infos_publiques'),
    path('profil/infos_privees/', PrivateDataUpdateView.as_view(), name='infos_privees'),
    path('profil/photo/', TemplateView.as_view(template_name="covoiturage/profil/photo.html"), name='photo'),
    path('profil/vehicule/', CarOwnerView.as_view(), name='vehicule'),
    path('profil/password/', change_password, name='password'),
    path('profil/preferences/', TemplateView.as_view(template_name="covoiturage/profil/preferences.html"), name="preferences"),
    
    path('profil/adresse/', AddressCreateView.as_view(), name="address"),
    path('profil/adresse/<int:pk>', AddressUpdateView.as_view(), name='address_update'),
    path('profil/adresse/<int:pk>/delete', AddressDeleteView.as_view(), name='address_delete'),

]