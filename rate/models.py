from django.db import models
from django.contrib.auth.models import User
from metrices.models import Metrices
# Create your models here.
class Rate(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rater')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    metric = models.ForeignKey(Metrices, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    pub_date = models.DateField(auto_now=True)