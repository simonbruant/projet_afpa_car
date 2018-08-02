from django import forms
from django.forms import TextInput, RadioSelect, Select, DateInput, FileInput, CheckboxInput

from .models import Car, FormationSession, AfpaCenter, Address
from users.models import PrivateData, User

class PrivateDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('phone_number', 'afpa_number')
        widgets = {
            'phone_number': TextInput(attrs={'class': 'form-control require-input'}),
            'afpa_number': TextInput(attrs={'class': 'form-control require-input' })
        }

    
class UserUpdateForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'email', 'trainee', 'driver_license', 'car_owner', 'afpa_center' )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control require-input'}),
            'first_name': TextInput(attrs={'class': 'form-control require-input'}),
            'last_name': TextInput(attrs={'class': 'form-control require-input'}),
            'email': TextInput(attrs={'class': 'form-control require-input'}),
            'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
            'driver_license': RadioSelect(attrs={'class': 'custom-control-input',
                                                }),
            'afpa_center': Select(attrs={'class': 'custom-select'}),
            'car_owner': RadioSelect(attrs={'class': 'custom-control-input'}),
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

class ProfilImageUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', )
    avatar = forms.ImageField(label='Company Logo', required=False,
                                error_messages ={'Erreur': "Seulement des fichiers images"},
                                widget=FileInput(attrs={'class': 'custom-file-input',
                                                        '@change': 'previewImage'}) )                               
    remove_avatar = forms.BooleanField(required=False,
                                        widget=CheckboxInput(attrs={'class': 'custom-control-input'}) )

    def save(self, commit=False, *args, **kwargs):
        obj = super(ProfilImageUpdateForm, self).save(commit=False, *args, **kwargs)
        if self.cleaned_data.get('remove_avatar'):
            print('ok')
            obj.avatar = None
            obj.save()
        else:
            obj.avatar = self.cleaned_data['avatar']
            obj.save()

        return obj

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

class AfpaCenterForm(forms.ModelForm):
    class Meta:
        model = AfpaCenter
        fields = ('center_name',)
        widgets = {
            'center_name': Select(attrs={'class': 'custom-select'}),
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
    address_label = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control require-input'}))

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
