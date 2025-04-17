from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
