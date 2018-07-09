from django.urls import path
from django.conf.urls import url

from covoiturage import views

urlpatterns = [
    
    path('', views.accueil),


]