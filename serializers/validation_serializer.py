from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.validators import *
class UserSerializer(serializers.Serializer):
    firstname=serializers.CharField(required=True,allow_blank=False,error_messages={
        'blank':'First Name cannot be empty',
    })
    firstname=serializers.CharField(required=True,allow_blank=False,error_messages={
        'blank':'First Name cannot be empty',
    })
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())],allow_blank=False,error_messages={
        'blank':'Email cannot be empty',
        'invalid':'Email is not a valid email address',
        
    })
    username=serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())],error_messages={
        'blank':'Username cannot be empty',
        
        
    })
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, required=False
    )  



