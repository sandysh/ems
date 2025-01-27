from django.db import models
from datetime import *
from django.contrib.auth.models import User
class WorkLog(models.Model):
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_log")
    missed_hours=models.DurationField(default=timedelta(0),null=True)
    redeemed_hours=models.DurationField(default=timedelta(0),null=True)
    remaining_hours=models.DurationField(default=timedelta(0),null=True)