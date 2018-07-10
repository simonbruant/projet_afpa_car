from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from .managers import UserManager

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True, verbose_name='email adress')
    username    = models.CharField(max_length=15, unique=True, verbose_name = 'pseudo')
    first_name  = models.CharField(max_length=30, verbose_name = 'prénom')
    last_name   = models.CharField(max_length=50, verbose_name = 'nom')
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    joined_date = models.DateTimeField(editable=False, default=timezone.now)
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

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active