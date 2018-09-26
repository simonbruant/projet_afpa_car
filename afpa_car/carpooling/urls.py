from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy, re_path
from django.views.generic import TemplateView, RedirectView
reverse_lazy
from .views import ( DashboardView, PrivateDataUpdateView, UserUpdateView, DefaultTripView, 
                    CarCreateView, CarUpdateView, CarDeleteView,
                    ProfilImageUpdateView, PreferencesUpdateView,
                    AddressCreateView, AddressUpdateView, AddressDeleteView, 
                    TripView, TripDetailView, PropositionView, PropositionRefusedView ,CounterPropositionView,
                    ContactView, AddressPOC, PropositionUpdateView)
from users.views import LoginView, ChangePassword
app_name = 'carpooling'

urlpatterns = [ 
    
    path('', LoginView.as_view(), name="index"),
    path('login/', RedirectView.as_view(url=reverse_lazy('carpooling:index')), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

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

    path('semaine-type/', DefaultTripView.as_view(), name='calendar'),
    
    path('trip/', TripView.as_view(), name="trip"),
    path('trip/<int:pk>/', TripDetailView.as_view(), name='trip_detail'),

    path('proposition/<int:pk>/', PropositionView.as_view(), name="proposition"),
    path('proposition_detail/<int:pk>/', PropositionUpdateView.as_view(), name="proposition_detail"),
    path('proposition_refused/<int:pk>/', PropositionRefusedView.as_view(), name="proposition_refused"),
    path('proposition_counter/<int:pk>/', CounterPropositionView.as_view(), name="proposition_counter"),

    path('addr_poc/', AddressPOC.as_view(), name="addr_poc"),


    path('cgu/', TemplateView.as_view(template_name='carpooling/cgu.html'), name='cgu'),
    path('contact/', ContactView.as_view(), name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

