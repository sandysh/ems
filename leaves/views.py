import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pendulum import datetime
from serializers.leaves_serializers import LeavesSerializer
from leaves.models import Leaves
from django_easy_validation import Validator
from django.utils.dateparse import parse_date
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

    try:
        leave_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    leave_serializer = LeavesSerializer(data=leave_data)
    if not leave_serializer.is_valid():
        return JsonResponse(leave_serializer.errors, status=422, safe=False)

 
    leave_date_range = leave_data.get('leave_date_range', '')
    try:
        date_range = leave_date_range.split(" to ")
        from_date, to_date = parse_date(date_range[0]), parse_date(date_range[1]) if len(date_range) > 1 else parse_date(date_range[0])
        if not from_date or not to_date:
            raise ValueError("Invalid date range")
    except (IndexError, ValueError):
        return JsonResponse({'error': 'Invalid leave_date_range format. Expected "YYYY-MM-DD to YYYY-MM-DD".'}, status=422)

    overlapping_leaves = Leaves.objects.filter(
        user_id=request.user.id,
        from_date__lte=to_date,
        to_date__gte=from_date,
    ).exclude(status__in=['REJECTED', 'CANCELLED'])

    if overlapping_leaves.exists():
        return JsonResponse({'error': 'You already have leaves either pending or approved for the applied dates.'}, status=422)

    try:
        leave_type = LeavesTypes.objects.get(id=leave_data['leave_type'])
    except LeavesTypes.DoesNotExist:
        return JsonResponse({'error': 'Invalid leave type provided.'}, status=422)

    total_leaves_taken = Leaves.objects.filter(
        user_id=request.user.id, 
        leave_type=leave_type, 
        status='APPROVED'
    ).count()

    if total_leaves_taken >= leave_type.days:
        return JsonResponse({'error': f'You cannot apply for more {leave_type.name} leave than you have been allotted.'}, status=422)

    leave_record = Leaves.objects.create(
        user=request.user,
        leave_type=leave_type,
        from_date=from_date,
        to_date=to_date,
        reason=leave_data['reason']
    )

    return JsonResponse({'success': 'Leave applied successfully.', 'leave_id': leave_record.id}, status=201)


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
