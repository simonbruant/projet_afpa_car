from django.db import models

from users.models import User

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=15, verbose_name = 'Code Postal',)

    def __str__(self):
        return str( self.zip_code )

    class Meta:
        verbose_name = "Code Postal"
        verbose_name_plural = "Codes Postaux"


class City(models.Model):
    city_name   = models.CharField(max_length=60, verbose_name = "Ville",)
    zip_codes   = models.ManyToManyField(ZipCode, verbose_name="Code Postal", through= "ZipCode_City")

    def __str__(self):
        return  self.city_name

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"


class ZipCode_City(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Villes")
    zip_code = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name="Code Postal", )

    def __str__(self):
        return "Choix :"

class Address(models.Model):
    address_label_public = models.CharField(max_length=50, verbose_name = "Libellé de l'adresse public", null=True, blank=True)
    street_number        = models.CharField(max_length=15, null=True, blank=True, verbose_name = "Numéro de la rue",)
    street_name          = models.CharField(max_length=100, verbose_name = "Nom de la rue",)
    street_complement    = models.CharField(max_length=100, null=True, blank=True, verbose_name = "Complément d'adresse",)
    zip_code             = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')
    city                 = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')

    # TODO : Avec Leaflet -> remettre Lattitude / Longitude en obligatoire (?) (généré par l'adresse)
    lattitude            = models.DecimalField(max_digits=25, decimal_places=25, null=True, blank=True, verbose_name = 'lattitude',)
    longitude            = models.DecimalField(max_digits=25, decimal_places=25, null=True, blank=True, verbose_name = 'longitude',)

    users                = models.ManyToManyField(User, verbose_name="Utilisateur", through= "Address_User")

    class Meta:
        verbose_name = "Adresse"

class Address_User(models.Model):
    address_label_private = models.CharField(max_length=100, default="Adresse", null=True, blank=True, verbose_name="Libellé privé")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="", )

    def __str__(self):
        return ""