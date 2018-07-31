from django import forms
from django.forms import TextInput, RadioSelect, Select, DateInput

from .models import Car, FormationSession, AfpaCenter
from users.models import PrivateData, User

class PrivateDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('phone_number', 'afpa_number')
        widgets = {
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'afpa_number': TextInput(attrs={'class': 'form-control'})
        }

    
class UserUpdateForm (forms.ModelForm):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ( 'username', 'first_name', 'last_name', 'email', 'trainee', 'driver_license', 'afpa_center' )
=======
        fields = ( 'username', 'first_name', 'last_name', 'email', 'trainee', 'driver_license', 'car_owner' )
>>>>>>> profil
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
            'driver_license': RadioSelect(attrs={'class': 'custom-control-input'}),
            'afpa_center': Select(attrs={'class': 'custom-select'}),
            'car_owner': RadioSelect(attrs={'class': 'custom-control-input'}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ( 'color', 'model', 'amount_of_free_seats', 'consumption','fuel' )
        widgets = {
            'color': TextInput(attrs={'class': 'form-control'}),
            'model': TextInput(attrs={'class': 'form-control'}),
            'amount_of_free_seats': TextInput(attrs={'class': 'form-control'}),
            'consumption': TextInput(attrs={'class': 'form-control'}),
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
                                    error_messages ={'invalid': "Image files only"},
                                    widget=forms.FileInput)    
    remove_avatar = forms.BooleanField(required=False)

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
