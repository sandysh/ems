from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(default=None, blank=True, null=True, max_length=500)
    punch_in_date = models.DateField(default=None, blank=True, null=True)
    punch_in_time = models.TimeField(default=None, blank=True, null=True)
    punch_out_date = models.DateField(default=None, blank=True, null=True)
    punch_out_time = models.TimeField(default=None, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(default=None, blank=True, null=True)
    hours_worked = models.DurationField(default=timedelta(0),null=True, blank=True)
