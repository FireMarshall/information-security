from django.db import models

# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=10)
    ip = models.CharField(max_length=20)

    def __str__(self):
        return self.username