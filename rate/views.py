import json
from django.shortcuts import render
from django.http import JsonResponse as response
from metrices.models import Metrices
from django.contrib.auth.models import User
from rate.models import Rate
from django.views.decorators.http import require_http_methods
from rest_framework import serializers
from django.db.models import Avg, Count

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
    newData = {
        "rater": request.user,
        "rated": rated,
        "metric": metric,
        "score": data['metric']['score'],
    }

    user = Rate.objects.create(**newData)
    return response('success', safe=False)


def getLatestRatings(request):
    ratings = Rate.objects.all().order_by('-id')[:20]
    ratings = FeedbackSerializer(ratings,many=True)
    return response(ratings.data, safe=False)


@require_http_methods(['GET'])
def getLeaderboard(request):
    try:
        leaderboard = Rate.objects.select_related('rated', 'metric').values(
            'rated__id', 
            'rated__first_name', 
            'rated__last_name',
            'metric__name'
        ).annotate(
            avg_score=Avg('score'),
            total_votes=Count('id')
        ).order_by('-avg_score')
        
        result = list(leaderboard)
        print(f"Leaderboard data: {result}")  # Debug print
        return response(result, safe=False)
    except Exception as e:
        print(f"Error in getLeaderboard: {e}")
        return response([], safe=False)