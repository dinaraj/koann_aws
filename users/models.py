from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    is_candidate = models.BooleanField(default=True)
    email = models.EmailField(_('Adresse mail'), unique=True)
    phone = models.CharField(_('Numéro de téléphone'), max_length=50, null=True, blank=True)
    linkedin = models.CharField(_("Profil Linkedin"), max_length=200, null=True, blank=True)
    picture = models.ImageField(_("Photo de profil"), upload_to='users/picture/', null=True, blank=True)
    resume = models.FileField(_('CV'), upload_to='users/resume/', null=True, blank=True)
    is_active = models.BooleanField(_("Actif"), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name = _("utilisateur")

    def __str__(self):
        if not self.first_name and not self.last_name:
            return self.email
        return self.get_full_name()
