from django import forms

from users.models import PrivateData

class PrivateDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('phone_number', 'afpa_number')

    
