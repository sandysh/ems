from django.db import models

# Create your models here.
class Metrices(models.Model):
    name = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)