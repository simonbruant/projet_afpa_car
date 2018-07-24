from django import forms
from django.forms import TextInput, RadioSelect

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
        fields = ( 'username', 'first_name', 'last_name', 'email','car_owner', 'trainee' )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'car_owner': RadioSelect(attrs={'class': 'custom-control-input'}),
            'trainee': RadioSelect(attrs={'class': 'custom-control-input'}),
        }

# (attrs={'class': 'custom-control-input'})