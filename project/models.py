from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_with_status')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='statuses')

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='task_with_status')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    attachments = ArrayField(models.FileField(upload_to='attachments/'), blank=True, default=list)

    def __str__(self):
        return self.title
