import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pendulum import datetime

from leaves.models import Leaves
from django_easy_validation import Validator
from helpers.general import is_ajax, serialize_data
from leaves.rules.leaves_rules import LeavesRules
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from helpers.general import make_pagination, make_serialized_pagination, dateMaker, date_list_from_date_range, date_splitter
from leaves_types.models import LeavesTypes
from serializers.leaves_serializers import LeavesSerializer
from array import array

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
    # return JsonResponse(dateFrags, safe=False)
    if len(dateRange) != 2:
        dateRange.append(str(dateRange[0]))
        # return JsonResponse(dateRange, safe=False)
    leaves = (Leaves.objects.filter(from_date__gte=dateRange[0], to_date__lte=dateRange[1])
              .exclude(status='REJECTED')
              .exclude(status='CANCELLED')
              .order_by('-id').values())

    if leaves:
        return JsonResponse({'error':'You already have leaves either pending or approved for the applied dates'},status=422, safe=False)
    # from_date = date_splitter(dateRange[0])
    # to_date = date_splitter(dateRange[1])
    # dates_list = date_list_from_date_range(datetime(from_date['year'],from_date['month'],from_date['day']), datetime(to_date['year'],to_date['month'],to_date['day']))
    leave_type = LeavesTypes.objects.get(id=leave['leave_type'])
    total_leaves_taken = Leaves.objects.filter(user_id=request.user.id,status='APPROVED').count()
    if total_leaves_taken >= leave_type.days:
        return JsonResponse({'error':'You cannot apply to more ' + leave_type.name + ' leave than you have been alloted'}, status=422, safe=False)
    newData = {
        "user": request.user,
        "leave_type_id": leave['leave_type'],
        "from_date": dateRange[0],
        "to_date": dateRange[1],
        "reason": leave['reason'],
    }
    Leaves.objects.create(**newData)
    return JsonResponse('success', safe=False)

@never_cache
def all(request):
    body = json.loads(request.body)
    leaves = None
    if body['range'] != "":
        range = dateMaker(body['range'])
        if range[0] and range[1]:
            if request.user.is_superuser:
                leaves = Leaves.objects.filter(created_at__date__range=[range[0],range[1]]).order_by('-id')
            else:
                leaves = Leaves.objects.filter(user_id=request.user.id, created_at__date__range=[range[0],range[1]]).order_by('-id')
        else:
            if request.user.is_superuser:
                leaves = Leaves.objects.filter(created_at__date=range[0]).order_by('-id')
            else:
                leaves = Leaves.objects.filter(user_id=request.user.id,created_at__date=range[0]).order_by('-id')
    else:
        if request.user.is_superuser:
            leaves = Leaves.objects.order_by('-id')
        else:
            leaves = Leaves.objects.filter(user=request.user).order_by('-id')

    if body['status'] != "all":
        leaves = leaves.filter(status=body['status'])
    paginated_data = make_serialized_pagination(request, leaves, LeavesSerializer)
    return JsonResponse(paginated_data, safe=False)


@never_cache
@require_http_methods('PUT')
@login_required
def update(request, leave_id):
    leave = json.loads(request.body)
    dateRange = leave['leave_date'].split(" to ")
    newData = {
        "leave_type": leave['leave_type'],
        "from_date": dateRange[0],
        "to_date": dateRange[1],
        "reason": leave['reason'],
    }
    Leaves.objects.filter(pk=leave_id).update(**newData)
    return JsonResponse({"status": "success", "message": "Leave updated successfully"}, safe=False)


@login_required
def updateStatus(request, leave_id):
    leave = json.loads(request.body)
    Leaves.objects.filter(pk=leave_id).update(status=leave['status'])
    return JsonResponse({"status": "success", "message": "Status updated successfully"}, safe=False)


@login_required
@require_http_methods('POST')
def stats(request):
    body = json.loads(request.body)
    generalLeaves = LeavesTypes.objects.filter(type='general').values()
    stats = {
        "total_leaves_applied": 0,
        "total_leaves_pending": 0,
        "total_leaves_approved": 0,
        "total_leaves_rejected": 0,
        "general": {

        }
    }

    if request.user.is_superuser:
        for i, l in enumerate(generalLeaves):
            name = l['name']
            stats['general'][i] = {
                "name": name,
                "approved": Leaves.objects.filter(
                    status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count(),
                "total": l['days']
            }
            # stats['general'][name] = Leaves.objects.filter(user=request.user).filter(
            #     status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count()
        stats["total_leaves_applied"] = Leaves.objects.order_by('-id').count()
        stats["total_leaves_pending"] = Leaves.objects.filter(status='PENDING').order_by(
            '-id').count()
        stats["total_leaves_approved"] = Leaves.objects.filter(
            status='APPROVED').order_by('-id').count()
        stats["total_leaves_rejected"] = Leaves.objects.filter(
            status='REJECTED').order_by('-id').count()
    else:
        for i,l in enumerate(generalLeaves):
            name = l['name']
            stats['general'][i] = {
                "name": name,
                "approved": Leaves.objects.filter(user=request.user).filter(
                     status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count(),
                "total": l['days']
            }
            # stats['general'][name] = Leaves.objects.filter(user=request.user).filter(
            #     status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count()
        stats["total_leaves_applied"] = Leaves.objects.filter(user=request.user).order_by('-id').count()
        stats["total_leaves_pending"] = Leaves.objects.filter(user=request.user).filter(status='PENDING').order_by(
            '-id').count()
        stats["total_leaves_approved"] = Leaves.objects.filter(user=request.user).filter(
            status='APPROVED').order_by('-id').count()
        stats["total_leaves_rejected"] = Leaves.objects.filter(user=request.user).filter(
            status='REJECTED').order_by('-id').count()
    return JsonResponse(stats,safe=True)
