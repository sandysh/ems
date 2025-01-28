from django.shortcuts import render
from .models import PollOptions
from poll.models import Poll
from serializers.poll_serializers import PollOptionsSerializer
# Create your views here.

def index(request):
    pass

def get_poll_options(request,poll_id):
    poll=Poll.objects.get(id=poll_id)
    poll_options=PollOptions.objects.filter(poll=poll)
    json_poll_options=PollOptionsSerializer(poll_options,many=True)
    return json_poll_options


def set_poll_options(request,poll_id,options):
    poll=Poll.objects.get(id=poll_id)
    for option in options:
        poll_options=PollOptions.objects.create(poll_id=poll_id,poll_options=option)
    return
