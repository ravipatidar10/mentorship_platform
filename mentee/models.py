# 3rd Party Import
from django.db import models
from django.contrib.auth.models import User


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " (mentee)"