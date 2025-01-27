from rest_framework import serializers
from rest_framework.validators import *
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['id','name']



# class UserSerializer(serializers.ModelSerializer):
#     groups = GroupSerializer(many=True)
#     class Meta:
#         model = User
#         fields = ['id','first_name','last_name', 'email','username','is_active','is_superuser','groups']



class UserSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True,allow_blank=False,error_messages={
        'blank':'First Name cannot be empty',
    })
    last_name=serializers.CharField(required=True,allow_blank=False,error_messages={
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
    is_superuser = serializers.BooleanField(
        required=False,
        default=False,
    )
    is_active = serializers.BooleanField(
        required=False,
        default=True,
    )
    