from django.contrib import admin

from .models import ZipCode_City, Adress_User, Address, ZipCode, City, Car, Car_User, Formation, FormationSession, AfpaCenter

class ZipCodeInline(admin.TabularInline):        
    model = ZipCode_City
    verbose_name = "Code Postal"
    verbose_name_plural = "Codes Postaux"
    extra = 1

class ZipCodeAdmin(admin.ModelAdmin):
    inlines = (ZipCodeInline, )

class CityInline(admin.TabularInline):
    model = ZipCode_City
    verbose_name = "Ville"
    verbose_name_plural = "Villes"
    extra = 1

class CityAdmin(admin.ModelAdmin):
    inlines = (CityInline,)

# ------------------------------

class AddressUserInLine(admin.TabularInline): # autre variante : admin.StackedInline
    model = Adress_User
    verbose_name = "Utilisateur de cette adresse"
    verbose_name_plural = "Utilisateurs de cette adresse"
    extra = 0


class AdressAdmin(admin.ModelAdmin):
    inlines = (AddressUserInLine,)
    list_display = ('adress_label', 'city', 'zip_code','street_number', 'street', 'get_users' )

    def get_users(self, obj):
        return " ; ".join([u.get_full_name() for u in obj.users.all()])
    get_users.short_description = 'Utilisateurs'

    search_fields = ('city__city_name', 'zip_code__zip_code', 'street', 'adress_label', 'users__first_name', 'users__last_name', )


class CarUserInLine(admin.TabularInline): # autre variante : admin.StackedInline
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

# class AfpaCenter(admin.ModelAdmin):
#     model = AfpaCenter

# Register your models here.
admin.site.register(Address, AdressAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(AfpaCenter, AfpaCenterAdmin)
admin.site.register(Formation)
admin.site.register(FormationSession)
