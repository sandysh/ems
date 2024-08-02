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


@never_cache
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

    if body['status'] != "all":
        leaves = leaves.filter(status=body['status'])
    paginated_data = make_serialized_pagination(request, leaves)
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
    stats = {
        "total_leaves_applied": 0,
        "total_leaves_pending": 0,
        "total_leaves_approved": 0,
        "total_leaves_rejected": 0,
    }
    if body['range'] != "":
        range = dateMaker(body['range'])
        if range[0] and range[1]:
            if request.user.is_superuser:
                stats["total_leaves_applied"] = Leaves.objects.filter(from_date__gte=range[0],
                                                                      to_date__lte=range[1]).order_by('-id').count()
                stats["total_leaves_pending"] = Leaves.objects.filter(from_date__gte=range[0],
                                                                      to_date__lte=range[1]).filter(
                    status='PENDING').order_by('-id').count()
                stats["total_leaves_approved"] = Leaves.objects.filter(from_date__gte=range[0],
                                                                       to_date__lte=range[1]).filter(
                    status='APPROVED').order_by('-id').count()
                stats["total_leaves_rejected"] = Leaves.objects.filter(from_date__gte=range[0],
                                                                       to_date__lte=range[1]).filter(
                    status='REJECTED').order_by('-id').count()
            else:
                stats["total_leaves_applied"] = Leaves.objects.filter(user_id=request.user.id, from_date__gte=range[0],
                                                                      to_date__lte=range[1]).order_by('-id').count()
                stats["total_leaves_pending"] = Leaves.objects.filter(user_id=request.user.id, from_date__gte=range[0],
                                                                      to_date__lte=range[1]).filter(
                    status='PENDING').order_by('-id').count()
                stats["total_leaves_approved"] = Leaves.objects.filter(user_id=request.user.id, from_date__gte=range[0],
                                                                       to_date__lte=range[1]).filter(
                    status='APPROVED').order_by('-id').count()
                stats["total_leaves_rejected"] = Leaves.objects.filter(user_id=request.user.id, from_date__gte=range[0],
                                                                       to_date__lte=range[1]).filter(
                    status='REJECTED').order_by('-id').count()
        else:
            if request.user.is_superuser:
                stats["total_leaves_applied"] = Leaves.objects.filter(from_date=range[0]).order_by('-id').count()
                stats["total_leaves_pending"] = Leaves.objects.filter(from_date=range[0]).filter(
                    status='PENDING').order_by('-id').count()
                stats["total_leaves_approved"] = Leaves.objects.filter(from_date=range[0]).filter(
                    status='APPROVED').order_by('-id').count()
                stats["total_leaves_rejected"] = Leaves.objects.filter(from_date=range[0]).filter(
                    status='REJECTED').order_by('-id').count()
            else:
                stats["total_leaves_applied"] = Leaves.objects.filter(user_id=request.user.id,
                                                                      from_date=range[0]).order_by('-id').count()
                stats["total_leaves_pending"] = Leaves.objects.filter(user_id=request.user.id,
                                                                      from_date=range[0]).filter(
                    status='PENDING').order_by('-id').count()
                stats["total_leaves_approved"] = Leaves.objects.filter(user_id=request.user.id,
                                                                       from_date=range[0]).filter(
                    status='APPROVED').order_by('-id').count()
                stats["total_leaves_rejected"] = Leaves.objects.filter(user_id=request.user.id,
                                                                       from_date=range[0]).filter(
                    status='REJECTED').order_by('-id').count()
    else:
        if request.user.is_superuser:
            stats["total_leaves_applied"] = Leaves.objects.order_by('-id').count()
            stats["total_leaves_pending"] = Leaves.objects.filter(status='PENDING').order_by('-id').count()
            stats["total_leaves_approved"] = Leaves.objects.filter(status='APPROVED').order_by('-id').count()
            stats["total_leaves_rejected"] = Leaves.objects.filter(status='REJECTED').order_by('-id').count()
        else:
            stats["total_leaves_applied"] = Leaves.objects.filter(user=request.user).order_by('-id')
            stats["total_leaves_pending"] = Leaves.objects.filter(user=request.user).filter(status='PENDING').order_by(
                '-id').count()
            stats["total_leaves_approved"] = Leaves.objects.filter(user=request.user).filter(
                status='APPROVED').order_by('-id').count()
            stats["total_leaves_rejected"] = Leaves.objects.filter(user=request.user).filter(
                status='REJECTED').order_by('-id').count()
    return JsonResponse(stats, safe=False)
