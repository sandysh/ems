from rest_framework import serializers
from rate.models import Rate
from metrices.models import Metrices
from django.contrib.auth.models import User


# class RatedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields= fields = ['first_name','last_name']

# class RaterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields= fields = ['first_name','last_name']
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']  


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrices
        fields= fields = ['id','name', 'score']

class RateSerializer(serializers.ModelSerializer):
    metric = MetricSerializer()
    rater = UsernameSerializer()
    # total_score = serializers.SerializerMethodField('total_metric_score')
    # rated = UsernameSerializer()
    class Meta:
        model = Rate
        fields = ['rater', 'metric','score']
        
        
        # print(obj.metric)
        # return obj.metric.objects.annotate(Sum('score'))
        # return obj.values('metric_id').annotate(sum=Sum('score'))
    
class UserSerializer(serializers.ModelSerializer):

    # rater = RateSerializer(many=True)
    rated = RateSerializer(many=True)
    sum_total = serializers.SerializerMethodField('sum_total_metrices')
    total_raters = serializers.SerializerMethodField('count_total_raters')
    metric_scores = serializers.SerializerMethodField('metric_total_score')
    # metrices = serializers.SerializerMethodField('ratings')
    class Meta:
        model = User
        fields = ['first_name','last_name', 'rated','sum_total', 'total_raters', 'metric_scores']       
    
    def sum_total_metrices(self, obj):
        from django.db.models import Sum
        all_data = obj.rated.all()
        score = all_data.aggregate(score = Sum('score'))
        return score
    
    def count_total_raters(self, obj):
        from django.db.models import Count, Sum
        all_data = obj.rated.all()
        total = all_data.aggregate(total = Count('rater'))
        return total


    def metric_total_score(self, obj):
        from django.db.models import Count, Sum
        all_data = obj.rated.all()
        score = all_data.values('metric').values('metric__name').annotate(score=Sum('metric__score'))
        metric_score = []
        for metric in score:
            # print(metric)
            metric_score.append(metric)
            # metric_score.append(Metrices.objects.filter(id=metric['metric']))
        return metric_score

