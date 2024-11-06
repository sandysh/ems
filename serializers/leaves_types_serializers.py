from rest_framework import serializers
from leaves_types.models import LeavesTypes

class LeavesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesTypes
        fields = ['id','name','days','type','status']