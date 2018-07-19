from django.urls import path
from django.views.generic import TemplateView

from users.views import LoginView

app_name = 'covoiturage'

urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil.html")),

]