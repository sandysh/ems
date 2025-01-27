from django.shortcuts import render
from .models import Settings
from serializers import settings_serializers
from django.http import JsonResponse,HttpResponse,response
import json
from helpers.general import *
# Create your views here.
def index(request):
    return render(request,'settings/index.html')

def get_settings(request):
    settings=Settings.objects.all()
    for setting in settings:
        if(setting.name=='punch_in_time'):
            data=am_pm(setting.values)
            setting.values=data[0]+"-"+data[1]
    serialized_data=settings_serializers.SettingsSerializers(settings,many=True)
    return JsonResponse(serialized_data.data,safe=False)


def update_setting(request,id):
    data = json.loads(request.body)
    value=data['values']
    setting=Settings.objects.get(id=id)
    setting.values=value
    setting.save()
    return JsonResponse('success', safe=False)

    
def get_punch_in_time():
     setting=Settings.objects.get(name="punch_in_time")
     values=setting.values.split("-")
     return [parse_time(values[0]),parse_time(values[1])]
def get_punch_out_time():
    setting=Settings.objects.get(name="punch_out_time")
    values=setting.values.split("-")[0]
    return values
def set_punch_in_time(data):
     setting=Settings.objects.get(name="punch_in_time")
     values=setting.values.split("-")
     return [parse_time(values[0]),parse_time(values[1])]

# def set_punch_out_time(data):
#     setting=Settings.objects.get(name="punch_out_time")
#     values=setting.values.split("-")[0]
#     return values
def get_working_hours():
    setting=Settings.objects.get(name="working_hours")
    working_hours=parse_duration(setting.values)
    return working_hours
def get_working_days():
    setting=Settings.objects.get(name="working_days")
    return setting.values

from datetime import datetime

def am_pm(range):
    values = range.split("-")
    start_time, finish_time = values[0], values[1]
    start = datetime.strptime(start_time, "%H:%M")
    finish = datetime.strptime(finish_time, "%H:%M")
    start_string = start.strftime("%I:%M %p")  
    finish_string = finish.strftime("%I:%M %p") 
    return [start_string, finish_string]
