# logs/models.py

from django.db import models
from django.contrib.auth.models import User


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LEAVE_APPLIED', 'Leave Applied'),
        ('LEAVE_APPROVED', 'Leave Approved'),
        ('LEAVE_REJECTED', 'Leave Rejected'),
        ('ATTENDANCE_MARKED', 'Attendance Marked'),
        ('PROFILE_UPDATED', 'Profile Updated'),
        ('LOGIN', 'User Logged In'),
        ('LOGOUT', 'User Logged Out'),
        ('ROLE_CHANGED', 'Role Changed'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at}] {self.user} - {self.action}"
