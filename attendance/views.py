import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import date, datetime, timedelta
from attendance.models import Attendance
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def dateMaker(range):
    fromDate = None
    toDate = None
    if "to" in range:
        range = range.split(" to ")
        date_format = '%Y-%m-%d'
        fromDate = datetime.strptime(range[0], date_format)
        toDate = datetime.strptime(range[1], date_format)

    else:
        date_format = '%Y-%m-%d'
        fromDate = datetime.strptime(range, date_format)
        toDate = fromDate 
    return [fromDate, toDate]



@login_required
def index(request):
    attendance = None
    buttonText = ''
    
    single_date = request.GET.get('date', '')

    if single_date:
        try:
            date_filter = datetime.strptime(single_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format.")
            date_filter = date.today()
    else:
        date_filter = date.today()

    try:
        attendance = Attendance.objects.filter(punch_in_date=date_filter, user_id=request.user.id).first()
    except Exception as e:
        print(f"An exception occurred: {e}")

    buttonText = 'Punch Out' if attendance else 'Punch In'

    users = User.objects.all()

    records = Attendance.objects.filter(punch_in_date=date_filter).select_related('user')

    attendance_records = []
    for user in users:
        user_record = {
            'user': user,
            'attendance': records.filter(user=user).first(),
        }
        attendance_records.append(user_record)

    context = {
        'users': users,
        'attendance_records': attendance_records,
        'today': date.today(),
        'now': datetime.now().strftime("%I:%M %p"),
        'attendance': attendance,
        'buttonText': buttonText,
        'single_date': single_date,
    }

    template = "attendance/admin/index.html" if request.user.is_superuser else "attendance/user/index.html"

    return render(request, template, context)


@login_required
def attendance_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    date_range = request.GET.get('date_range', '')
    from_date = None
    to_date = None

    if from_date and to_date:
        records = Attendance.objects.filter(
            user=user,
            punch_in_date__range=[from_date.date(), to_date.date()]
        ).select_related('user')
    else:
        today = date.today()
        start_date = today - timedelta(days=30)
        records = Attendance.objects.filter(
            user=user,
            punch_in_date__range=[start_date, today]
        ).select_related('user')

    context = {
        'user': user,
        'attendance_records': records,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(request, "attendance/admin/attendance_history.html", context)




@login_required
def attendance_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    date_range = request.GET.get('date_range', '')
    from_date = None
    to_date = None

    if date_range:
        try:
            from_date, to_date = dateMaker(date_range)
        except ValueError:
            print("Invalid date range format.")
            from_date = to_date = None

    if from_date and to_date:
        records = Attendance.objects.filter(
            user=user,
            punch_in_date__range=[from_date.date(), to_date.date()]
        ).select_related('user')
    else:
        today = date.today()
        start_date = today - timedelta(days=30)
        records = Attendance.objects.filter(
            user=user,
            punch_in_date__range=[start_date, today]
        ).select_related('user')

    context = {
        'user': user,
        'attendance_records': records,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(request, "attendance/admin/attendance_history.html", context)





@login_required
def punch(request):
    attendance = None
    newData = {}
    notes = request.POST.get('notes')
    today = date.today()
    now = datetime.now().strftime("%H:%M")
    try:
        attendance = Attendance.objects.filter(punch_in_date=date.today()).filter(user=request.user)
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
         range = dateMaker(range=filters['range'])

         if range[0] and range[1]:
            summaries = Attendance.objects.filter(user_id =request.user.id, punch_in_dategte=range[0], punch_in_datelte=range[1]).values()
         else:
            summaries = Attendance.objects.filter(user_id =request.user.id, punch_in_date=range[0]).values()
     else:
        summaries = Attendance.objects.filter(user_id =request.user.id).values()
     return JsonResponse(list(summaries), safe=False)

