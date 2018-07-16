from django.contrib import admin
from .models import * # TODO import seulement ce dont on a besoin

class ZipCodeInline(admin.TabularInline):        
    model = City.zip_codes.through
    verbose_name = "Code Postal"
    verbose_name_plural = "Codes Postaux"
    extra= 1

class ZipCodeAdmin(admin.ModelAdmin):
    # exclude = ("zipCode", ) # TODO : Virer exclude ?
    inlines = (ZipCodeInline, )



class CityInline(admin.TabularInline):
    model = City.zip_codes.through
    verbose_name = "Ville"
    verbose_name_plural = "Villes"
    
    extra = 1

class CityAdmin(admin.ModelAdmin):
    # exclude = ("zipCode", )
    inlines = (CityInline, )

# Register your models here.
admin.site.register(Address)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)