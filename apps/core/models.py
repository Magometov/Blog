from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя с персональными настройками"""
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    location = models.CharField(max_length=30, null=True, blank=True, verbose_name='Страна')
    birth_date = models.DateField(null=True, blank=True, verbose_name='День рождения')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')
    surname = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name if not self.first_name is None else ""} {self.surname if not self.surname is None else ""}'

    def __str__(self):
        return f'{self.id} {self.get_full_name()}'
