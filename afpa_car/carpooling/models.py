from django.conf import settings
from django.db import models


class Address(models.Model):
    city               = models.CharField(max_length=100, null=True, blank=True)
    zip_code           = models.CharField(max_length=20, null=True, blank=True)
    street_name        = models.CharField(max_length=200, null=True, blank=True)
    street_number      = models.CharField(max_length=10, null=True, blank=True)
    national_reference = models.CharField(max_length=20, null=True, blank=True)
    latitude           = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude          = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    address_label      = models.CharField(max_length=100, null=True, blank=True)
    user               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                            null=True, blank=True, related_name='addresses')

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
    
    def __str__(self):
        return self.address_label

class Car(models.Model):
    FUEL = (
        ('SP-98', 'SP-98'),
        ('SP-95', 'SP-95'),
        ('SP-95 E10', 'SP-95 E10'),
        ('DIESEL', 'DIESEL'),
        ('GPL', 'GPL'),
        ('ELECTRIQUE', 'ELECTRIQUE'),
    )

    color       = models.CharField(max_length=50, verbose_name="Couleur")
    model       = models.CharField(max_length=50, verbose_name="Modèle")
    consumption = models.FloatField(verbose_name="Consommation (en l/100km)", null=True, blank=True)
    fuel        = models.CharField(max_length=20, choices=FUEL, verbose_name="Type de carburant")    
    amount_of_free_seats = models.IntegerField(default=1, verbose_name="Nombre de places libres")

    users       = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cars', verbose_name="Utilisateur", through= "Car_User")

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return self.model

class Car_User(models.Model):
    car     = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Vehicule")
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="", )

    def __str__(self): 
        return ""

class AfpaCenter(models.Model):
    center_name = models.CharField(max_length=50, verbose_name="Nom du centre")
    address     = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")

    class Meta:
        verbose_name = "Centre AFPA"
        verbose_name_plural = "Centres AFPA"

    def __str__(self):
        return self.center_name

