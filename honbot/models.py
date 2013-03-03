from django.db import models

# Create your models here.

class Names(models.Model):
    account_id = models.PositiveIntegerField()
    name = models.CharField(max_length=30)