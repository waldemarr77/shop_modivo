from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Електронна пошта')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Номер телефону')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    city = models.CharField(max_length=50, null=True, blank=True,  verbose_name='Місто')


    class Meta:
        ordering = ['username']
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'


    def __str__(self):
        return self.username