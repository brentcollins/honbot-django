from django.db import models

# Create your models here.


class Names(models.Model):
    name = models.CharField(max_length=50)
    account_id = models.PositiveIntegerField()
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
