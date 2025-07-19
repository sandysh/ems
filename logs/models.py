# logs/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class ActionLog(models.Model):
    action = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_performed')
    action_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_received')
    data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model']),
            models.Index(fields=['action']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.model} by {self.action_by or 'System'}"

