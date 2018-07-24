from django import forms

from .models import Address, City

class AddressForm(forms.ModelForm):
    city = forms.CharField(label='city')
    zip  = forms.CharField(label='zip')

    class Meta:
        model = Address
        fields = ('address_label', 'street_number', 'street', 'street_complement', 'zip_code', )
        exclude = ['city', 'zip_code', 'lattitude', 'longitude', 'users']

    def save(self, commit=True):
        city = super(AddressForm, self).save(commit=True)
        if commit:
            city.save()
        return city

