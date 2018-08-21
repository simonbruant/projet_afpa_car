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

class DefaultTrip(models.Model):
    DAY = (
        ('Monday', 'Lundi'),
        ('Tuesday', 'Mardi'),
        ('Wednesday', 'Mercredi'),
        ('Thursday', 'Jeudi'),
        ('Friday', 'Vendredi'),
    )
    morning_departure_time          = models.DateTimeField(verbose_name="Heure de départ aller")
    morning_arriving_time           = models.DateTimeField(verbose_name="Heure d'arrivée aller")
    evening_departure_time          = models.DateTimeField(verbose_name="Heure de départ retour")
    evening_estimated_arriving_time = models.DateTimeField(verbose_name="Heure d'arrivée estimée retour")
    estimated_trip_cost             = models.IntegerField(editable=False, default=0, verbose_name="Coût du trajet estimé")
    day                 = models.CharField(max_length=10, choices=DAY, verbose_name="Nom du Jour")

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    has_for_start       = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="Départ", verbose_name="Adresse de Départ")
    has_for_destination = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="Destination", verbose_name="Adresse d'Arrivée")

    class Meta:
        verbose_name = "Trajet Type"
        verbose_name_plural = "Trajets Type"

    def __str__(self): 
        return "Trajet par défaut"

class Trip(DefaultTrip):

    trip_date = models.DateField(null=True, verbose_name="Jour du trajet")

    passenger = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='passengers', verbose_name="Passager", through= "Trip_Passenger")


    class Meta:
        verbose_name = "Trajet Particulier"
        verbose_name_plural = "Trajets Particuliers"

class Trip_Passenger(models.Model):
    validated_proposal = models.BooleanField(default=False, verbose_name='Proposition validée')

    trip    = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trajet")
    passenger    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Passager")

    def __str__(self): 
        return ""

class MeetingPoint(models.Model):
    public_or_private = models.BooleanField(default=False, verbose_name="Public ou privé",
                                        choices=( (True, "Public"), (False, 'Private')))

    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")

    class Meta:
        verbose_name = "Point de rencontre"
        verbose_name_plural = "Points de rencontre"

    def __str__(self): 
        return ""

class VisibleBy(models.Model):
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    meeting_point = models.ForeignKey(MeetingPoint, on_delete=models.CASCADE, verbose_name="Point de rencontre")

class Proposal(models.Model):
    proposal_date      = models.DateTimeField(null=True, verbose_name="Date de la proposition")
    is_validated       = models.BooleanField(default=False, verbose_name="Proposition validée")
    meeting_point_name = models.CharField(max_length=50, verbose_name="Nom du point de rencontre")

    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    meeting_point = models.ForeignKey(MeetingPoint, on_delete=models.CASCADE, verbose_name="Point de rencontre")

    class Meta:
        verbose_name = "Proposition"
        verbose_name_plural = "Propositions"

class IsAStep(models.Model):
    trip          = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trajet")
    meeting_point = models.ForeignKey(MeetingPoint, on_delete=models.CASCADE, verbose_name="Point de rencontre")
