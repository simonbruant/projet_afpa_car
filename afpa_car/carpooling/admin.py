from django.contrib import admin

from .models import ZipCode_City, Address_User, Address, ZipCode, City, Car, Car_User, Formation, FormationSession, AfpaCenter

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

class UserInLine(admin.TabularInline): # autre variante : admin.StackedInline
    model = Address_User
    verbose_name = "Utilisateur de cette adresse"
    verbose_name_plural = "Utilisateurs de cette adresse"
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    inlines = (UserInLine,)
    list_display = ('address_label', 'city', 'zip_code', 'street_name', 'street_number', 'get_users' )

    def address_label(self, obj):
        address_label_public = obj.address_label_public
        if address_label_public:
            return address_label_public
        else:
            address_user = Address_User.objects.filter(address=obj)
            return " ; ".join([addr.address_label_private for addr in address_user])
    address_label.short_description = "Libellé(s) de l'adresse"

    def get_users(self, obj):
        return " ; ".join([u.get_full_name() for u in obj.users.all()])
    get_users.short_description = 'Utilisateurs'

    search_fields = ('city__city_name', 'zip_code__zip_code',  'street_name', 'users__first_name', 'users__last_name', )


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

class FormationSessionAdmin(admin.ModelAdmin):
    model = FormationSession
    list_display = ('formation','formation_session_start_date', 'formation_session_end_date', 'work_experience_start_date', 'work_experience_end_date')



# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(AfpaCenter, AfpaCenterAdmin)
admin.site.register(Formation)
admin.site.register(FormationSession, FormationSessionAdmin)