from django.db import models
from datetime import timedelta
# Create your models here.
class Settings(models.Model):
    # punch_in_time=models.TimeField(auto_now_add=True,null=True)
    # punch_out_time=models.TimeField(auto_now_add=True,null=True)
    # working_hours=models.DurationField(default=timedelta(0),null=True) 
    name=models.CharField(default=None,max_length=250) 
    values=models.CharField(default=None,max_length=250) 