from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    
    path('', TemplateView.as_view(template_name="covoiturage/accueil.html")),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil.html")),

]