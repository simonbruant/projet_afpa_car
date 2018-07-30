from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager
from covoiturage.models import AfpaCenter

class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(max_length=255, unique=True, verbose_name='email adress')
    username        = models.CharField(max_length=15, unique=True, verbose_name='pseudo',)
    first_name      = models.CharField(max_length=30, verbose_name='prénom')
    last_name       = models.CharField(max_length=50, verbose_name='nom')
    driver_license  = models.BooleanField(default=False, verbose_name="permis",
                                        choices=( (True, "Oui"), (False, "Non")) )
    trainee         = models.BooleanField(default=False, verbose_name="statut",
                                        choices=( (True, "Stagiare"),(False, "Employé") ))
    car_owner       = models.BooleanField(default=False, verbose_name="propriétaire d'un véhicule",
                                        choices=( (True, "Oui"), (False, "Non")) )
    avatar          = models.ImageField(null=True, blank=True, upload_to='photos/')
    smoker          = models.BooleanField(default=False, verbose_name="Fumeur",
                                        choices=( (True, "Fumeur"), (False, 'Non Fumeur')))
    talker          = models.BooleanField(default=False, verbose_name="Bavard",
                                        choices=( (True, "Tres Bavard"), (False, 'Peu Bavard')))
    music          = models.BooleanField(default=False, verbose_name="Musique",
                                        choices=( (True, "Oui"), (False, 'Non')))

    is_active       = models.BooleanField(default=True, verbose_name='Utilisateur actif')
    is_staff        = models.BooleanField(default=False, verbose_name="Staff")
    is_admin        = models.BooleanField(default=False, verbose_name='Admin')
    date_joined     = models.DateTimeField(editable=False, default=timezone.now)

    afpa_center     = models.ForeignKey(AfpaCenter, null=True, blank=True, on_delete=models.SET_NULL)
    # confirm   = models.BooleanField(default=False)
    # confirmed_date = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip() # verif utilité de strip, enleve quels espaces ?

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """ Does the user have a specific permission? """
        return True

    def has_module_perms(self, app_label):
        """ Does the user have permission to view the app 'app_label' """
        return True

class PrivateData(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number    = models.CharField(max_length=15, null=True, default="0")
    afpa_number     = models.CharField(max_length=15, null=True, default="0")