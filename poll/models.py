from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Poll(models.Model):
    POLL_STATUS = [
        ("APPROVED","approved"),
        ("PENDING","pending"),
        ("REJECTED","rejected"),
        ("CANCELLED","cancelled"),
    ]
    name=models.CharField()
    description=models.TextField()
    created_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    status=models.CharField(choices=POLL_STATUS,default="PENDING")
    timestap=models.DateTimeField(auto_now_add=True)