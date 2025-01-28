from django.db import models
from poll.models import Poll
# Create your models here.

class PollOptions(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='poll')
    poll_options=models.CharField()