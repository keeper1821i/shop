from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    objects = True
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    phone_number = models.CharField(null=True, max_length=11)
    photo = models.ImageField(upload_to='photo/', default='photo/no_photo.jpg')


