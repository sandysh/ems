from rest_framework import serializers
from rate.models import Rate
from django.contrib.auth.models import User
from metrices.models import Metrices

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']  


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrices
        fields= fields = ['id','name', 'score']

class RatingSerializer(serializers.ModelSerializer):
    metric = MetricSerializer()
    rater = UsernameSerializer()
    rated = UsernameSerializer()
    class Meta:
        model = Rate
        fields = ['rater','rated', 'metric','score']