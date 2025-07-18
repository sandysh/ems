from django.db import models
from django.contrib.auth.models import User

class UserSupervisor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supervisor_relation',
        help_text="The user who is assigned a supervisor."
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members',
        help_text="The supervisor assigned to the user."
    )

    def __str__(self):
        return f"{self.user.username} → {self.supervisor.username if self.supervisor else 'No Supervisor'}"
