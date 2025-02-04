from rest_framework import serializers
from poll_options.models import PollOptions
from poll.models import Poll
from poll_stats.models import PollStats
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name', 'last_name', ]


class PollOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PollOptions
        fields=['id','poll_options']

class PollStatsSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    voted_on=serializers.SerializerMethodField()
    class Meta:
        model=PollStats
        fields=['id','user','voted_on']

    def get_voted_on(self,obj):
        return {'id':obj.option.id,'option':obj.option.poll_options}

class PollSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    options=PollOptionsSerializer(many=True,read_only=True)
    stats=PollStatsSerializer(many=True,read_only=True)
    class Meta:
        model=Poll
        fields=['id','name', 'description', 'created_by','created_at','status','options','stats']