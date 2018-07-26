from django import forms
from django.forms import TextInput, RadioSelect, Select

from .models import Car
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
        fields = ( 'username', 'first_name', 'last_name', 'email', 'trainee', 'driver_license', 'car_owner' )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
            'driver_license': RadioSelect(attrs={'class': 'custom-control-input'}),
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



