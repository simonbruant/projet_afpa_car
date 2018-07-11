from django.urls import path
from django.views.generic import TemplateView

from .views import LoginView, SignupView


app_name = 'users'

urlpatterns = [
    path ('login/', LoginView.as_view(), name='login'),
    path ('signup/', SignupView.as_view(), name='signup'),
    path ('reussi/', TemplateView.as_view(template_name='users/reussi.html'), name='reussi')
]