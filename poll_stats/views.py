from django.shortcuts import render
import json
from .models import *
from serializers.poll_serializers import *
# Create your views here.
def index(request):
    pass

def set_stats(request):
    data=json.loads(request.body)
    poll=Poll.objects.get(id=data["poll_id"])
    option=PollOptions.objects.get(id=data["option_id"])
    stats=PollStats.objects.create(user=request.user,poll=poll,option=option)
    return stats

def get_stats_all(request):
    poll_stats=PollStats.objects.all()
    serialized_data=PollStatsSerializer(poll_stats,many=True)
    

