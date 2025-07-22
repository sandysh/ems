import json
from django.shortcuts import render
from django.http import JsonResponse as response
from metrices.models import Metrices
from django.contrib.auth.models import User
from rate.models import Rate
from django.views.decorators.http import require_http_methods
from rest_framework import serializers
from django.db.models import Avg, Count, Subquery, OuterRef
from logs.utils import log_action
from django.contrib.auth.models import Group
from django.utils.timezone import now
 
today = now()
current_year = today.year
current_month = today.month

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"
        depth = 1

@require_http_methods('GET')
def index(request):
    return render(request,'rate/index.html')


@require_http_methods('POST')
def store(request):
    data = json.loads(request.body)
    rated = User.objects.get(id=data['user']['id'])
    metric = Metrices.objects.get(id=data['metric']['id'])
    rater = request.user
    score = data['metric']['score']

    today = now()
    current_year = today.year
    current_month = today.month

    # Check if rating exists this month
    already_rated = Rate.objects.filter(
        rater=rater,
        rated=rated,
        metric=metric,
        pub_date__year=current_year,
        pub_date__month=current_month
    ).exists()

    if already_rated:
        return response('fail', safe=False)

    user = Rate.objects.create(rater=rater,rated=rated,metric=metric,score=score)

    # Log the rating action
    log_action(
        action="User Rated",
        model="Rate",
        action_by=request.user,
        action_to=rated,
        old={},
        new={
            "rated_id": rated.id,
            "metric_id": metric.id,
            "score": data['metric']['score']
        }
    )
    return response('success', safe=False)


def getLatestRatings(request):
    ratings = Rate.objects.all().order_by('-id')[:20]
    ratings = FeedbackSerializer(ratings,many=True)
    return response(ratings.data, safe=False)


# @require_http_methods(['GET'])
# def getLeaderboard(request):
#     try:
#         leaderboard = Rate.objects.select_related('rated', 'metric').values(
#             'rated__id', 
#             'rated__first_name', 
#             'rated__last_name',
#             'metric__name'
#         ).annotate(
#             avg_score=Avg('score'),
#             total_votes=Count('id')
#         ).order_by('-avg_score')
        
#         result = list(leaderboard)
#         print(f"Leaderboard data: {result}")  # Debug print
#         return response(result, safe=False)
#     except Exception as e:
#         print(f"Error in getLeaderboard: {e}")
#         return response([], safe=False)



@require_http_methods(['GET'])
def getLeaderboard(request):
    try:
        # Subquery to get the first group name for each user
        group_subquery = Group.objects.filter(user=OuterRef('rated__id')).values('name')[:1]
        
        leaderboard = Rate.objects.select_related('rated', 'metric').values(
            'rated__id', 
            'rated__first_name', 
            'rated__last_name',
            'metric__name'
        ).annotate(
            department=Subquery(group_subquery),  # Add department as group name
            avg_score=Avg('score'),
            total_votes=Count('id')
        ).order_by('-avg_score')
        
        result = list(leaderboard)
        print(f"Leaderboard data: {result}")  # Debug print
        return response(result, safe=False)
    except Exception as e:
        print(f"Error in getLeaderboard: {e}")
        return response([], safe=False)