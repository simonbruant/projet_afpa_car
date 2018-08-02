from django import forms
from django.forms import TextInput, RadioSelect, Select, DateInput, FileInput, CheckboxInput

from .models import Car, FormationSession, AfpaCenter, Address
from users.models import PrivateData, User


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

        
class UserUpdateForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'email', 'trainee', 'driver_license', 'car_owner', 'afpa_center' )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control require-input'}),
            'first_name': TextInput(attrs={'class': 'form-control require-input'}),
            'last_name': TextInput(attrs={'class': 'form-control require-input'}),
            'email': TextInput(attrs={'class': 'form-control require-input'}),
            'afpa_center': Select(attrs={'class': 'custom-select'}),
            'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
            'driver_license': RadioSelect(attrs={'class': 'custom-control-input'}),
            'car_owner': RadioSelect(attrs={'class': 'custom-control-input'}),
        }
        labels = {
            'username': 'Pseudonyme',
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse Email',
            'afpa_center': 'Centre AFPA',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ( 'color', 'model', 'amount_of_free_seats', 'consumption','fuel' )
        widgets = {
            'color': TextInput(attrs={'class': 'form-control require-input'}),
            'model': TextInput(attrs={'class': 'form-control require-input'}),
            'amount_of_free_seats': TextInput(attrs={'class': 'form-control require-input'}),
            'consumption': TextInput(attrs={'class': 'form-control require-input'}),
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

class ProfilImageUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', )
    avatar = forms.ImageField(label='Image de Profil', required=False,
                                    error_messages ={'invalid': "Importer uniquement un fichier .png ou .jpg"},
                                    widget=FileInput(attrs={'class': 'custom-file-input',
                                                        '@change': 'previewImage'}))    
    remove_avatar = forms.BooleanField(label="Supprimer l'avatar", required=False, 
                                        widget=CheckboxInput(attrs={'class': 'custom-control-input'}))

    def save(self, commit=False, *args, **kwargs):
        user = super(ProfilImageUpdateForm, self).save(commit=False, *args, **kwargs)
        if self.cleaned_data.get('remove_avatar'):
            user.avatar = None
            user.save()
        else:
            user.avatar = self.cleaned_data['avatar']
            user.save()
        return user

class FormationSessionForm(forms.ModelForm):
    class Meta:
        model = FormationSession
        fields = ('formation_session_start_date', 'formation_session_end_date', 'work_experience_start_date', 'work_experience_end_date')
        widgets = {
            'formation_session_start_date': DateInput(attrs={'type': 'date','class': 'form-control'}),
            'formation_session_end_date': DateInput(attrs={'type': 'date','class': 'form-control'}),
            'work_experience_start_date': DateInput(attrs={'type': 'date','class': 'form-control'}),
            'work_experience_end_date': DateInput(attrs={'type': 'date','class': 'form-control'}),
        }

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('smoker', 'talker', 'music')
        widgets = {
            'smoker': RadioSelect(),
            'talker': RadioSelect(),
            'music': RadioSelect(),
        }

class AddressForm(forms.ModelForm):
    address_label = forms.CharField(label="Libellé de l'adresse", required=False, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta: 
        model = Address
        fields = ('street_number', 'street_name', 'street_complement', 'zip_code', 'city')
        exclude = ['lattitude', 'longitude', ]
        widgets = {
            'street_number': TextInput(attrs={'class': 'form-control require-input'}),
            'street_name': TextInput(attrs={'class': 'form-control require-input'}),
            'street_complement': TextInput(attrs={'class': 'form-control'}),
            'zip_code': Select(attrs={'class': 'custom-select'}),
            'city': Select(attrs={'class': 'custom-select'}),
        }
        labels = {
            'street_number': 'Numéro de la Rue' ,
            'street_name': 'Nom de la Rue',
            'street_complement': "Complément de l'Adresse",
            'zip_code': 'Code Postal',
            'city': 'Ville',
        }



    # ## VERIFICATION DE LA PRESENCE DE L'ADRESSE DANS LA BDD LORS DE LA CREATION    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     address_label = cleaned_data.get("address_label") 
    #     street_number = cleaned_data.get("street_number") 
    #     street_name = cleaned_data.get("street_name") 
    #     street_complement = cleaned_data.get("street_complement") 
    #     zip_code = cleaned_data.get("zip_code") 
    #     city = cleaned_data.get("city") 
    #     rslt = Address.objects.filter(address_label=address_label, street_number=street_number, 
    #                                     street_name=street_name, street_complement=street_complement, 
    #                                     zip_code=zip_code, city=city)
    #     if rslt.count() :
    #         print( "adresse exxite déjà")
    #         raise forms.ValidationError("Cette adresse existe déjà")
    #     else :
    #         print( "adresse créée")
