from django.contrib import admin

from .models import Address, Car, AfpaCenter, DefaultTrip, Trip, Proposition, Register

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'zip_code', 'street_name', 'street_number' )

class CarAdmin(admin.ModelAdmin):
    model = Car
    list_display = ('model', 'user')
    
class AfpaCenterAdmin(admin.ModelAdmin):
    model = AfpaCenter
    list_display = ('center_name','address')

# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(AfpaCenter, AfpaCenterAdmin)
admin.site.register(DefaultTrip)
admin.site.register(Trip)
admin.site.register(Proposition)
admin.site.register(Register)


