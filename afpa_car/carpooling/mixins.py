import json
from carpooling.models import Address

class AddressMixin:

    def form_valid(self, form):
        print('valid')
        address = Address()
        print("eeeeeee", form.cleaned_data.get('json_hidden'))
        json_data = json.loads(form.cleaned_data.get('json_hidden'))
        geo = json_data['geometry']
        prop = json_data['properties']
        user = self.request.user 
        address_label = form.cleaned_data['address_label']

        address.user = user
        address.address_label = address_label.capitalize()
        address.longitude = geo['coordinates'][0]
        address.latitude = geo['coordinates'][1]
        address.city = prop['city']
        address.zip_code = prop['postcode']
        street = prop.get('street')
        street_number = prop.get('housenumber')
        name = prop.get('name')
        if street and street_number:
            address.street_number = street_number
            address.street_name = street
        else:
            address.street_name = name
        
        address.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)