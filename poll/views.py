from django.shortcuts import render
from .models import Poll
import json
from django.urls import *
from django.http import JsonResponse
from poll_options.views import *
from serializers.poll_serializers import *
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request,'poll/index.html')


def get_polls(request):
    db_poll=Poll.objects.all()
    polls=PollSerializer(db_poll,many=True)
    return JsonResponse(polls.data,safe=False)


def set_polls(request):
    data = json.loads(request.body)
    user=User.objects.get(id=request.user.id)
    poll_data={'name':data['name'],
               'description':data['description'],
               }
    serializer = PollSerializer(data=poll_data)
    if not serializer.is_valid():
        return JsonResponse({'error': serializer.errors}, status=400)
    poll_data.update({'created_by':user})
    poll = Poll.objects.create(**poll_data)
    if poll:
        set_poll_options(request, poll.id, data['options'])  
    return JsonResponse({'success': True})

def get_progess(request):
    pass


