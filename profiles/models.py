from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)
    about_me = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    signed_up = models.DateField(auto_now_add=True)   # datum vytvoření profilu # todo smazat
    last_online = models.DateField(auto_now=True)     # datum, kdy byl naposledy online

    first_name_private = models.BooleanField(default=False, null=False)
    last_name_private = models.BooleanField(default=False, null=False)
    about_me_private = models.BooleanField(default=False, null=False)
    email_private = models.BooleanField(default=False, null=False)
    birth_date_private = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.user.username


