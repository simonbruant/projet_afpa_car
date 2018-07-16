from django.contrib import admin
from .models import * # TODO import seulement ce dont on a besoin -> ZipCode_City ++

class ZipCodeInline(admin.TabularInline):        
    model = City.zip_codes.through
    verbose_name = "Code Postal"
    verbose_name_plural = "Codes Postaux"
    extra= 1

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

class UserInLine(admin.TabularInline): # autre variante : StackedInline
    model = Adress_User
    verbose_name = "Utilisateur"
    fk_name = "address"
    extra = 1

class AdressAdmin(admin.ModelAdmin):
    inlines = (UserInLine,)

# Register your models here.
admin.site.register(Address, AdressAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)