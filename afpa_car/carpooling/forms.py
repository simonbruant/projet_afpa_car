from functools import partial, wraps

from django import forms
from django.forms import TextInput, RadioSelect, Select, DateInput, FileInput, CheckboxInput, TimeInput, CheckboxSelectMultiple, modelformset_factory

from .models import Car, AfpaCenter, Address, DefaultTrip
from users.models import PrivateData, User, UserProfile


class PrivateDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('afpa_number', 'phone_number')

    phone_number = forms.RegexField(regex=r'^[0+][\d]+$', label="Numéro de Téléphone",
                                    min_length=10, max_length=13, 
                                    error_messages={'invalid': 'Numéro de téléphone invalide'}, 
                                    widget=TextInput(attrs={'class': 'form-control require-input'}))

    afpa_number = forms.RegexField( regex=r'^\d+$', label="Identifiant AFPA",
                                    min_length=8, max_length=8,
                                    error_messages={'invalid': 'Le numéro AFPA est composé de chiffres'}, 
                                    widget=TextInput(attrs={'class': 'form-control require-input'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'email',)
        widgets = {
            'username': TextInput(attrs={'class': 'form-control require-input'}),
            'first_name': TextInput(attrs={'class': 'form-control require-input'}),
            'last_name': TextInput(attrs={'class': 'form-control require-input'}),
            'email': TextInput(attrs={'class': 'form-control require-input'}),
        }
        labels = {
            'username': 'Pseudonyme',
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse Email',   
        }

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('trainee', 'driver_license', 'car_owner', 'afpa_center', 'gender',)
        widgets = {
                'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
                'driver_license': RadioSelect(attrs={'class': 'custom-control-input'}),
                'car_owner': RadioSelect(attrs={'class': 'custom-control-input'}),
                'afpa_center': Select(attrs={'class': 'custom-select'}),
                'gender': Select(attrs={'class': 'custom-select'})
        }
        labels = { 
            'afpa_center': 'Centre AFPA',
            'gender': 'Genre',
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ( 'color', 'model', 'amount_of_free_seats', 'consumption', 'fuel')
        widgets = {
            'color': TextInput(attrs={'class': 'form-control require-input'}),
            'model': TextInput(attrs={'class': 'form-control require-input'}),
            'amount_of_free_seats': TextInput(attrs={'class': 'form-control require-input'}),
            'consumption': TextInput(attrs={'class': 'form-control'}),
            'fuel': Select(attrs={'class': 'custom-select'}),
        }
        error_messages = {
            'consumption': {
                'invalid': ("Saisir un nombre"),
            },
        }
        labels = {
            'color': 'Couleur',
            'model': 'Modèle de ma voiture',
            'amount_of_free_seats': 'Nombre de places disponibles',
            'consumption': 'Consommation (L/100km)',
            'fuel': 'Carburant',
        }

    def clean_amount_of_free_seats(self):
        amount_of_free_seats = int(self.cleaned_data['amount_of_free_seats'])
        if amount_of_free_seats < 1:
            raise forms.ValidationError('Il doit y avoir au moins une place de libre dans votre véhicule')
        return amount_of_free_seats

    def clean_consumption(self):
        consumption = int(self.cleaned_data['consumption'])
        if consumption < 1:
            raise forms.ValidationError('Le nombre entré est incorrect')
        return consumption

class ProfilImageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_image', )

    profile_image = forms.ImageField(label='Image de Profil', required=False,
                                    error_messages ={'invalid': "Importer uniquement un fichier .png ou .jpg"},
                                    widget=FileInput(attrs={'class': 'custom-file-input',
                                                        '@change': 'previewImage'}))    
    remove_profile_image = forms.BooleanField(label="Supprimer l'avatar", required=False, 
                                        widget=CheckboxInput(attrs={'class': 'custom-control-input'}))

    def save(self, commit=False, *args, **kwargs):
        user_profile = super().save(commit=False, *args, **kwargs)
        
        if self.cleaned_data['remove_profile_image']:
            default_image = user_profile._meta.get_field('profile_image').get_default()
            user_profile.profile_image = default_image
            user_profile.save()
        else:
            user_profile.profile_image = self.cleaned_data['profile_image']
            user_profile.save()
        return user_profile

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('smoker', 'talker', 'music')
        widgets = {
            'smoker': RadioSelect(),
            'talker': RadioSelect(),
            'music': RadioSelect(),
        }

class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zip_code'].required = True
        self.fields['city'].required = True
        self.fields['street_name'].required = True

    class Meta: 
        model = Address
        fields = ('zip_code', 'city', 'street_number', 'street_name', 'address_label')
        widgets = {
            'zip_code': TextInput(attrs={'class': 'form-control require-input'}),
            'city': TextInput(attrs={'class': 'form-control require-input'}),
            'street_number': TextInput(attrs={'class': 'form-control'}),
            'street_name': TextInput(attrs={'class': 'form-control require-input'}),
            'address_label': TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'zip_code': 'Code Postal',
            'city': 'Ville',
            'street_number': 'Numéro de la Rue' ,
            'street_name': 'Nom de la Rue',
            'address_label': "Libellé de l'Adresse",
        }

class DefaultTripForm(forms.ModelForm):

    has_for_start = forms.ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'custom-select'}), 
                                                 label="Départ", required=False )
                                                
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['has_for_start'].queryset = Address.objects.filter(user=user)

    class Meta:
        model = DefaultTrip
        fields =('morning_departure_time', 'morning_arriving_time', 'evening_departure_time','has_for_start', 'deactivate' )
        widgets = {
            'morning_departure_time': TimeInput(attrs={'type': 'time', 'class': 'form-control require-input'}),
            'morning_arriving_time': TimeInput(attrs={'type': 'time', 'class': 'form-control require-input'}),
            'evening_departure_time': TimeInput(attrs={'type': 'time', 'class': 'form-control require-input'}),
            'deactivate': CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-control require-input'}),
        }

DefaultTripFormSet = modelformset_factory(DefaultTrip ,form=DefaultTripForm,
                                        extra=5, max_num=5, 
                                        fields = ('morning_departure_time', 'morning_arriving_time', 
                                                    'evening_departure_time','has_for_start', 'deactivate'))

class ContactForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse Email'}), 
                            label='Adresse Email',)
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}))
    subject = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet du Message'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre Message'}))
