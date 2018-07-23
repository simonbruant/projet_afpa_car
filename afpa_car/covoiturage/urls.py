from django.urls import path
from django.views.generic import TemplateView

from .views import DashboardView, CalendarView
from users.views import LoginView, LogoutView, signup_view

app_name = 'covoiturage'
urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil/infos_publiques.html"), name='profil'),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil/infos_publiques.html"), name='infos_publiques'),
    path('profil/infos_privees/', TemplateView.as_view(template_name="covoiturage/profil/infos_privees.html"), name='infos_privees'),
    path('profil/photo/', TemplateView.as_view(template_name="covoiturage/profil/photo.html"), name='photo'),
    path('profil/vehicule/', TemplateView.as_view(template_name="covoiturage/profil/vehicule.html"), name='vehicule'),
    path('profil/password/', TemplateView.as_view(template_name="covoiturage/profil/password.html"), name='password'),
    path('profil/preferences/', TemplateView.as_view(template_name="covoiturage/profil/preferences.html"), name="preferences"),
    path('profil/adresse/', TemplateView.as_view(template_name="covoiturage/profil/adresse.html"), name="adresse"),

]