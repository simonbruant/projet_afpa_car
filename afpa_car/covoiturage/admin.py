from django.contrib import admin
from .models import *


class ZipCodeInline(admin.TabularInline):        
    model = City.zipCode.through
    verbose_name = "Code Postal"
    verbose_name_plural = "Codes Postaux"
        
class ZipCodeAdmin(admin.ModelAdmin):
    exclude = ("zipCode", )
    inlines = (ZipCodeInline, )

class CityInline(admin.TabularInline):
    model = City.zipCode.through
    verbose_name = u"Ville"

class CityAdmin(admin.ModelAdmin):
    exclude = ("zipCode", )
    inlines = (CityInline, )


# Register your models here.
admin.site.register(Address)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)