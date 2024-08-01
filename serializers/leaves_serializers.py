from rest_framework import serializers
from leaves.models import Leaves
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class leavesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Leaves
        fields = ['id','leave_type','from_date', 'to_date','reason','user','status']