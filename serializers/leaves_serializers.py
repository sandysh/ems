from rest_framework import serializers
from leaves.models import Leaves
from leaves_types.models import LeavesTypes
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class LeavesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesTypes
        fields = ['id','name','days','type','status']

class LeavesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    leave_type = LeavesTypesSerializer()
    class Meta:
        model = Leaves
        fields = ['id','from_date', 'to_date','reason','user','leave_type','status','created_at','updated_at']