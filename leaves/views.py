import json
from datetime import date, datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from leaves.models import Leaves
from django_easy_validation import Validator
from helpers.general import is_ajax
from leaves.rules.leaves_rules import LeavesRules
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from helpers.general import make_pagination, make_serialized_pagination, dateMaker


def index(request):
    return render(request, "leaves/index.html")


@never_cache
@require_http_methods('POST')
@login_required
def store(request):
    errors = Validator.validate(request, LeavesRules.valid_rules, LeavesRules.messages)
    if errors and is_ajax:
        return JsonResponse(errors, status=422, safe=False)
    leave = json.loads(request.body)
    dateRange = leave['leave_date_range'].split(" to ")
    newData = {
        "user": request.user,
        "leave_type": leave['leave_type'],
        "from_date": dateRange[0],
        "to_date": dateRange[1],
        "reason": leave['reason'],
    }
    Leaves.objects.create(**newData)
    return JsonResponse('success', safe=False)


def all(request):
    body = json.loads(request.body)
    leaves = None
    if body['range'] != "":
        range = dateMaker(body['range'])
        if range[0] and range[1]:
            if request.user.is_superuser:
                leaves = Leaves.objects.filter(from_date__gte=range[0],
                                               to_date__lte=range[1]).order_by('-id')
            else:
                leaves = Leaves.objects.filter(user_id=request.user.id, from_date__gte=range[0],
                                           to_date__lte=range[1]).order_by('-id')
        else:
            if request.user.is_superuser:
                leaves = Leaves.objects.filter(from_date=range[0]).order_by('-id')
            else:
                leaves = Leaves.objects.filter(user_id=request.user.id, from_date=range[0]).order_by('-id')
    else:
        if request.user.is_superuser:
            leaves = Leaves.objects.order_by('-id')
        else:
            leaves = Leaves.objects.filter(user=request.user).order_by('-id')
    paginated_data = make_serialized_pagination(request, leaves)
    return JsonResponse(paginated_data, safe=False)


@never_cache
@require_http_methods('PUT')
@login_required
def update(request, leave_id):
    leave = json.loads(request.body)
    dateRange = leave['leave_date_range'].split(" to ")
    newData = {
        "leave_type": leave['leave_type'],
        "from_date": dateRange[0],
        "to_date": dateRange[1],
        "reason": leave['reason'],
    }
    Leaves.objects.filter(pk=leave_id).update(**newData)
    return JsonResponse('success', safe=False)


def updateStatus(request, leave_id):
    leave = json.loads(request.body)
    Leaves.objects.filter(pk=leave_id).update(status=leave['status'])
    return JsonResponse('success', safe=False)
