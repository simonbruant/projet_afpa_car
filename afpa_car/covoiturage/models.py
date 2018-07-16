from django.db import models

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
        return str( self.zip_code ) + " " + rslt
    class Meta:
        verbose_name = "Code Postal"
        verbose_name_plural = "Codes Postaux"

class City(models.Model):
    city_name   = models.CharField(max_length =25, verbose_name = "Ville",)
    zipCode     = models.ManyToManyField(ZipCode, verbose_name="Code Postal")

    def __str__(self):
        return  self.city_name
    class Meta:
        verbose_name = "Ville"


# class City_ZipCode(models.Model):
    

class Address(models.Model):
    adress_label        = models.CharField(max_length=50, verbose_name = "Libellé de l'adresse",)
    street              = models.TextField(max_length=50, verbose_name = "Nom de la rue",)
    street_number       = models.CharField(max_length = 30, null=True, blank = True, verbose_name = "Numéro de la rue",)
    street_complement   = models.CharField(max_length =50, null=True, blank = True, verbose_name = "Complément d'adresse",)
    # TODO : Verif Null et blank True or False
    lattitude           = models.DecimalField(max_digits=25, decimal_places=25, null=False, verbose_name = 'lattitude',)
    longitude           = models.DecimalField(max_digits=25, decimal_places=25, null=False, verbose_name = 'longitude',) # valeur imprécise -> seulement anti-abus
    # doc DecimalField : https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.DecimalField.max_digits

    # clé étrangere tjr dans l'entité qui a x,1 en cardinalité
    city    = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')
    zipCode = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')
    # ForeignKey == OneToMany
    class Meta:
        verbose_name = "Adresse"






    # civility = models.CharField(_('Status'), max_length = 20, blank = True)
    # firstname = models.CharField(_('Firstname'), max_length = 50, blank = True)
    # lastname = models.CharField(_('Lastname'), max_length = 50, blank = True)
    # departement = models.CharField(_('Departement'), max_length = 50, blank = True)
    # corporation = models.CharField(_('Corporation'), max_length = 100, blank = True)
    # building = models.CharField(_('Building'), max_length = 20, blank = True)
    # floor = models.CharField(_('Floor'), max_length = 20, blank = True)
    # door = models.CharField(_('Door'), max_length = 20, blank = True)
    # number = models.CharField(_('Number'), max_length = 30, blank = True)
    # street_line1 = models.CharField(_('Address 1'), max_length = 100, blank = True)
    # street_line2 = models.CharField(_('Address 2'), max_length = 100, blank = True)
    # zipcode = models.CharField(_('ZIP code'), max_length = 5, blank = True)
    # city = models.CharField(_('City'), max_length = 100, blank = True)
    # state = models.CharField(_('State'), max_length = 100, blank = True)

    # # French specifics fields
    # cedex = models.CharField(_('CEDEX'), max_length = 100, blank = True)
    
    # postal_box = models.CharField(_('Postal box'), max_length = 20, blank = True)
    # country = models.CharField(_('Country'), max_length = 100, blank = True)