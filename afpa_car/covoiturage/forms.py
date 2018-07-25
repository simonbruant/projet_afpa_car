from django import forms

from .models import Address, City
from django.forms import TextInput, RadioSelect

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address_label', 'street_number', 'street_name', 'street_complement', 'zip_code', 'city')
        exclude = ['lattitude', 'longitude', ]
        widgets = {
            'address_label': TextInput(attrs={'class': 'form-control'}),

        }
    
    def clean(self):
        cleaned_data = super().clean()

        address_label = cleaned_data.get("address_label") 
        street_number = cleaned_data.get("street_number") 
        street_name = cleaned_data.get("street_name") 
        street_complement = cleaned_data.get("street_complement") 
        zip_code = cleaned_data.get("zip_code") 
        city = cleaned_data.get("city") 

        rslt = Address.objects.filter(address_label=address_label, street_number=street_number, 
                                        street_name=street_name, street_complement=street_complement, 
                                        zip_code=zip_code, city=city)
        if rslt.count() :
            print( "adresse exxite déjà")
            raise forms.ValidationError("Cette adresse existe déjà")
        else :
            print( "adresse créée")