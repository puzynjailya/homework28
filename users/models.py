from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200, blank=False)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=8, decimal_places=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Локации'


class User(AbstractUser):
    ROLES = [
        ('admin', 'Администратор ОПГ'),
        ('member', 'Участиник ОПГ'),
        ('moderator', 'Смотрящий за ОПГ'),
    ]
    id = models.AutoField(editable=False, unique=True, primary_key=True, auto_created=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=75, blank=False)
    username = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=9, choices=ROLES, blank=False)
    age = models.SmallIntegerField(blank=False)
    location = models.ManyToManyField(Location)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
