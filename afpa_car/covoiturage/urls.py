from django.urls import path
from django.views.generic import TemplateView

from .views import DashboardView, PrivateDataUpdateView, UserUpdateView, CarCreateView, CarUpdateView
from users.views import LoginView, LogoutView, signup_view

app_name = 'covoiturage'
urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profil/', UserUpdateView.as_view(), name='profil'),
    path('profil/infos_publiques/', UserUpdateView.as_view(), name='infos_publiques'),
    path('profil/infos_privees/', PrivateDataUpdateView.as_view(), name='infos_privees'),
    path('profil/photo/', TemplateView.as_view(template_name="covoiturage/profil/photo.html"), name='photo'),
    path('profil/vehicule/', CarCreateView.as_view(), name='vehicule'),
    path('profil/vehicule/update/<int:pk>/', CarUpdateView.as_view(), name='vehicule_update'),
    path('profil/password/', TemplateView.as_view(template_name="covoiturage/profil/password.html"), name='password'),
    path('profil/preferences/', TemplateView.as_view(template_name="covoiturage/profil/preferences.html"), name="preferences"),
    path('profil/adresse/', TemplateView.as_view(template_name="covoiturage/profil/adresse.html"), name="adresse"),

]