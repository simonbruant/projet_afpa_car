from django.db import models

from users.models import User

class ZipCode(models.Model):
    zip_code = models.IntegerField( verbose_name = 'Code Postal',)
    
    def __str__(self):
        rslt = ""
        nb = 0
        for c in self.city_set.all(): # _set.all
            if nb != 0:
                rslt += " ; "
            rslt += str( c )
            nb += 1
        return str( self.zip_code )# + " " + rslt
    class Meta:
        verbose_name = "Code Postal"
        verbose_name_plural = "Codes Postaux"


class City(models.Model):
    city_name   = models.CharField(max_length =25, verbose_name = "Ville",)
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
    adress_label        = models.CharField(max_length=50, verbose_name = "Libellé de l'adresse",)
    street_number       = models.CharField(max_length=30, null=True, blank=True, verbose_name = "Numéro de la rue",)
    street              = models.CharField(max_length=50, verbose_name = "Nom de la rue",)
    street_complement   = models.CharField(max_length=50, null=True, blank=True, verbose_name = "Complément d'adresse",)

    # clé étrangere tjr dans l'entité qui a x,1 en cardinalité
    city    = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')
    zipCode = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')

    # TODO : Verif Null et blank True or False
    lattitude           = models.DecimalField(max_digits=25, decimal_places=25, null=True, blank=True, verbose_name = 'lattitude',)
    longitude           = models.DecimalField(max_digits=25, decimal_places=25, null=True, blank=True, verbose_name = 'longitude',) # valeur imprécise -> seulement anti-abus
    # doc DecimalField : https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.DecimalField.max_digits

    # ForeignKey == OneToMany
    users   = models.ManyToManyField(User, verbose_name="Utilisateur", through= "Adress_User")

    # TODO : Liaison Adress to User
    
    class Meta:
        verbose_name = "Adresse"
    def __str__(self):
        return  "{} -> adresse: {} {} {} {} ".format(self.adress_label, self.street_number, self.street,self.zipCode, self.city, )

class Adress_User(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=" ", )

    def __str__(self):
        return ""