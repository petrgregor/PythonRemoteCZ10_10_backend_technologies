from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=45, null=False)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False)
    private = models.BooleanField(null=False, default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=False)
    file = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f"User: { self.user } { self.created }: { self.body[0:50] }"


class MessageFile(models.Model):
    file = models.TextField(null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=False)


class MyUser(User):
    birthdate = models.DateField(null=True)

