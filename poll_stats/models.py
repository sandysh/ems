from django.db import models
from poll.models import Poll
from poll_options.models import PollOptions
from django.contrib.auth.models import User
# Create your models here.

class PollStats(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='user_info')
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='poll_info')
    option=models.ForeignKey(PollOptions,on_delete=models.CASCADE,related_name='poll_info')