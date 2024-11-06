from django.db import models

# Create your models here.
class LeavesTypes(models.Model):
    name = models.CharField(max_length=200)
    days = models.IntegerField()
    type = models.CharField(max_length=250)
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'leaves_types'