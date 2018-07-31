from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

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

    def __str__(self):
        return self.adress_label

class Address_User(models.Model):
    address_label_private   = models.CharField(max_length=100, default="Adresse", null=True, blank=True, verbose_name="Libellé privé")
    address                 = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="", )

    def __str__(self):
        return ""

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
    consumption = models.FloatField(verbose_name="Consommation (en l/100km)")
    fuel        = models.CharField(max_length=20, choices=FUEL, verbose_name="Type de carburant")    
    amount_of_free_seats = models.IntegerField(default=1, verbose_name="Nombre de places libres")

    users       = models.ManyToManyField(User, verbose_name="Utilisateur", through= "Car_User")

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return self.model


class Car_User(models.Model):
    car     = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Vehicule")
    user    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="", )

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

class Formation(models.Model):
    formation_name = models.CharField(max_length=50, verbose_name="Libellé de la Formation")

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return self.formation_name

class FormationSession(models.Model):
    formation_session_start_date    = models.DateField(verbose_name="Date de début de formation")
    formation_session_end_date      = models.DateField(verbose_name="Date de fin de formation")
    work_experience_start_date      = models.DateField(verbose_name="Date de début de stage")
    work_experience_end_date        = models.DateField(verbose_name="Date de fin de stage")
    
    formation  = models.ForeignKey(Formation, on_delete=models.CASCADE, verbose_name="Formation")

    class Meta:
        verbose_name = "Session de formation"
        verbose_name_plural = "Sessions de formations"

    def __str__(self):
        return ""

