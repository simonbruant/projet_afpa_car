from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView, RedirectView
reverse_lazy
from .views import ( DashboardView, PrivateDataUpdateView, UserUpdateView, CalendarView, 
                    CarCreateView, CarUpdateView, CarDeleteView,
                    ProfilImageUpdateView, PreferencesUpdateView,
                    AddressCreateView, AddressUpdateView, AddressDeleteView )
from users.views import LoginView, ChangePassword

app_name = 'carpooling'

urlpatterns = [ 
    
    path('', LoginView.as_view(), name="index"),
    path('login/', RedirectView.as_view(url=reverse_lazy('carpooling:index')), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('cgu/', TemplateView.as_view(template_name='carpooling/cgu.html'), name='cgu'),

    path('profil/infos-generales/', UserUpdateView.as_view(), name='general_infos'),
    path('profil/infos-privees/', PrivateDataUpdateView.as_view(), name='private_infos'),
    path('profil/photo/', ProfilImageUpdateView.as_view(), name='photo'),
    path('profil/password/', ChangePassword.as_view(), name='password'),
    path('profil/preferences/', PreferencesUpdateView.as_view(), name="preferences"),
    
    path('profil/vehicule/', CarCreateView.as_view(), name='car'),
    path('profil/vehicule/<int:pk>/', CarUpdateView.as_view(), name='car_update'),
    path('profil/vehicule/<int:pk>/delete', CarDeleteView.as_view(), name='car_delete'),
    
    path('profil/adresse/', AddressCreateView.as_view(), name="address"),
    path('profil/adresse/<int:pk>', AddressUpdateView.as_view(), name='address_update'),
    path('profil/adresse/<int:pk>/delete', AddressDeleteView.as_view(), name='address_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
