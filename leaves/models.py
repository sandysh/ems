from django.db import models
from django.contrib.auth.models import User

class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    LEAVES_TYPES = [
    ("CASUAL", "casual"),
    ("SICK", "sick"),
    ]
    leave_type = models.CharField(choices=LEAVES_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    LEAVES_STATUS = [
        ("APPROVED","approved"),
        ("PENDING","pending"),
        ("REJECTED","rejected"),
        ("CANCELLED","cancelled"),
    ]
    status = models.CharField(choices=LEAVES_STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    