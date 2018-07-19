from django.urls import path
from django.views.generic import TemplateView

from users.views import LoginView, SignupView, LogoutView

app_name = 'covoiturage'

urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('profil/', TemplateView.as_view(template_name="covoiturage/profil.html")),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reussi/', TemplateView.as_view(template_name='covoiturage/reussi.html'), name='reussi'),
    path('logout/', LogoutView.as_view(), name='logout'),
]