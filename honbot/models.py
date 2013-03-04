from django.db import models


class Names(models.Model):
    account_id = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
