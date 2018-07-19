from django.urls import path
from django.views.generic import TemplateView

app_name = 'covoiturage'
urlpatterns = [
    
    path('', TemplateView.as_view(template_name="covoiturage/accueil.html")),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil.html"), name='profil'),
    path('profil/infos_publiques/', TemplateView.as_view(template_name="covoiturage/profil/infos_publiques.html"), name='infos_publiques'),
    path('profil/infos_privees/', TemplateView.as_view(template_name="covoiturage/profil/infos_privees.html"), name='infos_privees'),
    path('profil/photo/', TemplateView.as_view(template_name="covoiturage/profil/photo.html"), name='photo'),
    path('profil/vehicule/', TemplateView.as_view(template_name="covoiturage/profil/vehicule.html"), name='vehicule'),
    path('profil/password/', TemplateView.as_view(template_name="covoiturage/profil/password.html"), name='password'),
    path('profil/preferences/', TemplateView.as_view(template_name="covoiturage/profil/preferences.html"), name="preferences"),
    path('profil/adresse/', TemplateView.as_view(template_name="covoiturage/profil/adresse.html"), name="adresse"),

]