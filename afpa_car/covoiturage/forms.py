from django import forms

from users.models import PrivateData, User

# class PrivateDataUpdateForm(forms.ModelForm):
#     class Meta:
#         model = PrivateData
#         fields = ('phone_number', 'afpa_number')

    
class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('car_owner', )
        widgets = {
            'car_owner': forms.RadioSelect
        }