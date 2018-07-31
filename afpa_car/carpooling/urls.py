from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from .views import ( DashboardView, PrivateDataUpdateView, UserUpdateView, CalendarView, 
                    CarCreateView, CarUpdateView, CarDeleteView, ProfilRedirectview, 
                    ProfilImageUpdateView, PreferencesUpdateView, 
                    AddressCreateView, AddressUpdateView, AddressDeleteView )
from users.views import LoginView, LogoutView, signup_view, change_password

app_name = 'carpooling'

urlpatterns = [
    
    path('', LoginView.as_view(), name="index"),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('calendar/', CalendarView.as_view(), name='calendar'),

    path('profil/', ProfilRedirectview.as_view(), name='profil'),
    path('profil/infos-generales/', UserUpdateView.as_view(), name='general_infos'),
    path('profil/infos-privees/', PrivateDataUpdateView.as_view(), name='private_infos'),
    path('profil/photo/', ProfilImageUpdateView.as_view(), name='photo'),
    path('profil/password/', change_password, name='password'),
    path('profil/preferences/', PreferencesUpdateView.as_view(), name="preferences"),
    
    path('profil/vehicule/', CarCreateView.as_view(), name='car'),
    path('profil/vehicule/<int:pk>/', CarUpdateView.as_view(), name='car_update'),
    path('profil/vehicule/<int:pk>/delete', CarDeleteView.as_view(), name='car_delete'),
    
    path('profil/adresse/', AddressCreateView.as_view(), name="address"),
    path('profil/adresse/<int:pk>', AddressUpdateView.as_view(), name='address_update'),
    path('profil/adresse/<int:pk>/delete', AddressDeleteView.as_view(), name='address_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
