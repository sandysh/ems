from django.db import models
from django.contrib.auth.models import User
from leaves_types.models import LeavesTypes


class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    leave_type = models.ForeignKey(LeavesTypes,on_delete=models.DO_NOTHING)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    LEAVES_STATUS = [
        ("APPROVED","approved"),
        ("PENDING","pending"),
        ("REJECTED","rejected"),
        ("CANCELLED","cancelled"),
    ]
    status = models.CharField(choices=LEAVES_STATUS, default="PENDING", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    