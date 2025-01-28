from rest_framework import serializers
from leaves.models import Leaves
from leaves_types.models import LeavesTypes
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class LeavesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesTypes
        fields = ['id', 'name', 'days', 'type', 'status']

class LeavesSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  
    leave_type = serializers.PrimaryKeyRelatedField(queryset=LeavesTypes.objects.all()) 
    # reason = serializers.CharField(
    #     required=True, 
    #     allow_blank=False, 
    #     error_messages={'blank': 'Reason Field is required'}
    # )
    # from_date = serializers.DateField(
    #     required=True, 
    #     error_messages={'blank': "From Date Field is required"}
    # )
    # to_date = serializers.DateField(
    #     required=False, 
    # )

    class Meta:
        model = Leaves
        fields = ['id', 'from_date', 'to_date', 'reason', 'user', 'leave_type', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'reason': {
                'required': True,
                'error_messages': {'blank': 'Reason field is required'},
            },
            'from_date': {
                'required': True,
                'error_messages': {'blank': 'From Date field is required'},
            },
            'to_date': {
                'required': False,
                'error_messages': {'blank': 'To Date field is required'},
            },
        }
