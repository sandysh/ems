from datetime import *
from .models import WorkLog
from helpers.general import time_difference,time_sum
from settings.views import *
def index(request):
    pass

 
def store_worklog(user, hours_worked:timedelta):
    prev_worklog = WorkLog.objects.filter(user=user).order_by('-date').first()
    prev_remaining = prev_worklog.remaining_hours if prev_worklog else timedelta(hours=0, minutes=0)
    current_date = date.today()
    standard_work_time = get_working_hours()

    if hours_worked > standard_work_time:
        surplus = time_difference(standard_work_time, hours_worked)
        new_remaining = max(prev_remaining - surplus, timedelta(hours=0)) 
        WorkLog.objects.create(
            date=current_date, 
            user=user, 
            redeemed_hours=surplus,
            remaining_hours=new_remaining 
        )
    else:
        missed = time_difference(standard_work_time, hours_worked)
        new_remaining = time_sum(prev_remaining, missed)
        WorkLog.objects.create(
            date=current_date, 
            user=user, 
            missed_hours=missed, 
            remaining_hours=new_remaining  
        )
    return True


def time_to_timedelta(time_obj):
    return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

def format_time(t):
    hours = t.seconds // 3600
    minutes = (t.seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"
