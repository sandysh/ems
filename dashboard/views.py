from django.shortcuts import render
from django.contrib.auth.models import User
from leaves.models import Leaves
from datetime import datetime
from attendance.models import Attendance
from metrices.models import Metrices
from django.db.models import Sum, Count
from rate.models import Rate
from .user_serializer import UserSerializer
from .rating_serializer import RatingSerializer
from django.http import JsonResponse, HttpResponse
import pendulum
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'dashboard.html')

def stats(request):
    users_all = User.objects.filter(is_staff=False)
    leaves_applied = Leaves.objects.filter(created_at__date=datetime.today().date()).count()
    present_today = Attendance.objects.filter(punch_in_date=datetime.today().date()).count()
    context = {
        "total_users" : users_all.count(),
        "leaves_applied": leaves_applied,
        "present_today": present_today,
        "absent_today": users_all.count() - present_today,
    }
    return JsonResponse({"data":context}, safe=False)

def points(request):
    period = request.GET.get('period', 'weekly')
    dt = pendulum.now()
    
    if period == 'weekly':
        start_date = dt.start_of('week').date()
        end_date = dt.end_of('week').date()
    else:  # monthly
        start_date = dt.start_of('month').date()
        end_date = dt.end_of('month').date()

    users_all = User.objects.filter(is_staff=False,)
    users =  UserSerializer(users_all, many=True).data
    rate = Rate.objects.select_related().all()
    metrices = Metrices.objects.all()
    
    # Filter ratings by date range using pub_date 
    ratings = Rate.objects.filter(
        pub_date__range=[start_date, end_date]
    )[:10]
    ratings =  RatingSerializer(ratings, many=True).data
    
    context = {
        "metrices": list(metrices.values()),
        "users": users,
        "rate": list(rate.values()),
        "ratings": ratings
    }
    return JsonResponse({"data":context}, safe=False)