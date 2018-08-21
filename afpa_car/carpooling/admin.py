from django.contrib import admin

from .models import Address, Car, Car_User, AfpaCenter

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'zip_code', 'street_name', 'street_number' )

class CarUserInLine(admin.TabularInline):
    model = Car_User
    verbose_name = "Utilisateur de ce véhicule"
    verbose_name_plural = "Utilisateurs de ce véhicule"
    extra = 0

class CarAdmin(admin.ModelAdmin):
    model = Car
    inlines = (CarUserInLine,)

    def get_users(self, obj):
        return " ; ".join([u.get_full_name() for u in obj.users.all()])
    get_users.short_description = 'Utilisateurs'

class AfpaCenterAdmin(admin.ModelAdmin):
    model = AfpaCenter
    list_display = ('center_name','address')



# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(AfpaCenter, AfpaCenterAdmin)
