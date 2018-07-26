from django import forms
from django.forms import TextInput, RadioSelect, Select


from .models import Address, City
from users.models import User

class CarOwnerForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('car_owner', )
        widgets = {
            'car_owner': forms.RadioSelect
        }


class AddressForm(forms.ModelForm):
    class Meta: 
        model = Address
        fields = ('address_label', 'street_number', 'street_name', 'street_complement', 'zip_code', 'city')
        exclude = ['lattitude', 'longitude', ]
        ## DOC List Widget : https://docs.djangoproject.com/en/1.8/_modules/django/forms/widgets/
        widgets = {
            'address_label': TextInput(attrs={'class': 'form-control'}),
            'street_number': TextInput(attrs={'class': 'form-control'}),
            'street_name': TextInput(attrs={'class': 'form-control'}),
            'street_complement': TextInput(attrs={'class': 'form-control'}),
            # TODO : Trouver équivalent du widget pour menu déroulant (FK) ou auto-completion de la ville/zipcode
            'zip_code': Select(attrs={'class': 'form-control'}),
            'city': Select(attrs={'class': 'form-control'}),
        }

    ## VERIFICATION DE LA PRESENCE DE L'ADRESSE DANS LA BDD LORS DE LA CREATION    
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
