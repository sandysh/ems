import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import date, datetime
from attendance.models import Attendance
from django.views.decorators.http import require_http_methods

def index(request):
    attendance = None
    allAttendance = Attendance.objects.filter(user_id =request.user.id).values()
    try:
        attendance = Attendance.objects.get(punch_in_date=date.today())
    except:
        print("An exception occurred")
    buttonText = ''
    if attendance:
        buttonText = 'Punch Out'
    else:
       buttonText = 'Punch In'
    context = {
        'today': date.today(),
        'now' : datetime.now().strftime("%I:%M %p"),
        'buttonText': buttonText,
        'attendance': attendance,
        'allAttendance': allAttendance
    }   
    return render(request,"attendance/index.html", context)

def punch(request):
    attendance = None
    newData = {}
    notes = request.POST.get('notes')
    today = date.today()
    now = datetime.now().strftime("%I:%M")
    try:
        attendance = Attendance.objects.filter(punch_in_date=date.today())
    except:
        print("An exception occurred")
    if attendance:
        attendance.update(punch_out_date = today, punch_out_time = now )
    else:
        newData = {
            "notes": notes,
            "punch_in_date": today,
            "punch_in_time": now,
            "user": request.user
        }
        attendance = Attendance.objects.create(**newData)
    return HttpResponseRedirect('/attendance/')


@require_http_methods('POST')
def summary(request):
     summaries = None
     body = json.loads(request.body)
     filters = body['filter']
     if filters['range'] != "":
         if "to" in filters['range']:
            range = filters['range'].split(" to ")
            date_format = '%Y-%m-%d'
            fromDate = datetime.strptime(range[0], date_format)
            toDate = datetime.strptime(range[1], date_format)
            summaries = Attendance.objects.filter(user_id =request.user.id, punch_in_date__gte=fromDate, punch_in_date__lte=toDate).values()
         else:
            date_format = '%Y-%m-%d'
            fromDate = datetime.strptime(filters['range'], date_format)
            summaries = Attendance.objects.filter(user_id =request.user.id, punch_in_date=fromDate).values()       
     else:      
        summaries = Attendance.objects.filter(user_id =request.user.id).values()
     return JsonResponse(list(summaries), safe=False)