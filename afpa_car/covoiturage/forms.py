from django import forms

from .models import Address, City

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address_label', 'street_number', 'street', 'street_complement', 'zip_code', 'city')
        exclude = ['lattitude', 'longitude', ]