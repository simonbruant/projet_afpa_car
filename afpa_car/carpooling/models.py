from django.conf import settings
from django.db import models


class Address(models.Model):
    city               = models.CharField(max_length=100, null=True, blank=True)
    zip_code           = models.CharField(max_length=20, null=True, blank=True)
    street_name        = models.CharField(max_length=200, null=True, blank=True)
    street_number      = models.CharField(max_length=10, null=True, blank=True)
    latitude           = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude          = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    address_label      = models.CharField(max_length=100, null=True, blank=True)
    user               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                            null=True, blank=True, related_name='addresses')

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
    
    def __str__(self):
        return self.address_label if self.address_label else "Adresse"

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

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cars', verbose_name="Utilisateur", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return self.model

class AfpaCenter(models.Model):
    center_name = models.CharField(max_length=50, verbose_name="Nom du centre")
    address     = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse", related_name='addresses')

    class Meta:
        verbose_name = "Centre AFPA"
        verbose_name_plural = "Centres AFPA"

    def __str__(self):
        return self.center_name

class DefaultTrip(models.Model):
    DAY = (
        ('Monday', 'Lundi'),
        ('Tuesday', 'Mardi'),
        ('Wednesday', 'Mercredi'),
        ('Thursday', 'Jeudi'),
        ('Friday', 'Vendredi'),
    )
    morning_departure_time          = models.TimeField(null=True, blank=True, verbose_name="Heure de départ")
    morning_arriving_time           = models.TimeField(null=True, blank=True, verbose_name="Heure d'arrivée")
    evening_departure_time          = models.TimeField(null=True, blank=True, verbose_name="Heure de retour")
    evening_estimated_arriving_time = models.TimeField(null=True, verbose_name="Arrivée estimée à")
    estimated_trip_cost             = models.IntegerField(editable=False, default=0, verbose_name="Coût du trajet estimé")
    day                             = models.CharField(null=True, max_length=10, choices=DAY, verbose_name="Jour")
    deactivate                      = models.BooleanField(default=False, verbose_name="désactivation" )
    user_is_driver                  = models.BooleanField(default=False, verbose_name="conducteur",)

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="default_trips" ,verbose_name="Utilisateur")
    has_for_start       = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="start", verbose_name="Départ")
    has_for_destination = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="destination", verbose_name="Destination")
    passengers          = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Register' ,related_name='passenger')

    class Meta:
        verbose_name = "Trajet Type"
        verbose_name_plural = "Trajets Type"

    def __str__(self): 
        return "Trajet type de {0} du {1}" .format(self.user.get_full_name(), self.day)

class Trip(DefaultTrip):
    trip_date = models.DateField(null=True, verbose_name="Jour du trajet")

    class Meta:
        verbose_name = "Trajet Particulier"
        verbose_name_plural = "Trajets Particuliers"

class Proposition(models.Model):
    # first_user = createur de la proposition
    # second_user = celui qui reçoit la proposition
    validated_proposal = models.BooleanField(default=False, verbose_name='Proposition validée')

    trip            = models.ForeignKey(Trip, on_delete=models.CASCADE, 
                                null=True, blank=True,verbose_name="Trajet", related_name='trip')
    default_trip    = models.ForeignKey(DefaultTrip, on_delete=models.CASCADE,
                                        null=True, blank=True, verbose_name="Trajet", related_name='default_trip')
    first_user       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name="First User", related_name='first_user')
    second_user      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name="Second User", related_name='second_user')
    message          = models.CharField(max_length=400)

    

    def __str__(self): 
        return "Proposition de " #+ self.passenger

class Register(models.Model):
    #ici ce trouve les passagers
    trip = models.ForeignKey(DefaultTrip, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)