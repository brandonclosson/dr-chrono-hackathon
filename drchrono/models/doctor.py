from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    api_id = models.IntegerField()
