from django import forms

from .models import * # TODO import selectif

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ('address_label', 'street_number', 'street', 'street_complement', 'city', 'zip_code',)