from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    telegram_id = models.CharField(max_length=100, blank=True)
    is_freelancer = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
