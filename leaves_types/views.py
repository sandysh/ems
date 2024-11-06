from django.shortcuts import render
from serializers import leaves_types_serializers
from leaves_types.models import LeavesTypes
from django.http import JsonResponse
# Create your views here.
def index(request):
    types =  LeavesTypes.objects.all()
    serializer = leaves_types_serializers.LeavesTypesSerializer(types, many=True)
    return JsonResponse(serializer.data, safe=False)