from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Subscription(models.Model):
    team_name = models.CharField(max_length=100, verbose_name='Назва команди')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Користувач')

    def __str__(self):
        return self.team_name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @staticmethod
    def get_absolute_url():
        return reverse("home")

    class Meta:
        verbose_name = 'Підписки'
        verbose_name_plural = 'Підписки'
        ordering = ['team_name']
