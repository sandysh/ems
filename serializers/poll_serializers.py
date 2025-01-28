from rest_framework import serializers
from poll_options.models import PollOptions
from poll.models import Poll
from poll_stats.models import PollStats
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name', ]

class PollSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Poll
        fields=['id','name', 'description', 'created_by','timestamp']

class PollOptionsSerializer(serializers.ModelSerializer):
    poll=PollSerializer()
    class Meta:
        model=PollOptions
        fields=['id','poll','poll_options']

class PollStatsSerializer(serializers.ModelSerializer):
    poll=PollSerializer()
    option=PollOptionsSerializer()
    class Meta:
        model=PollStats
        fields=['id','poll','option']