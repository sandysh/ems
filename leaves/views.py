import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pendulum import datetime
from serializers.leaves_serializers import LeavesSerializer
from leaves.models import Leaves
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
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def index(request):
    return render(request, "leaves/index.html")

@login_required
def supervisors(request):
    """Get all users with supervisor role"""
    try:
        supervisor_group = Group.objects.get(name='supervisor')
        supervisors = User.objects.filter(groups=supervisor_group).values('id', 'first_name', 'last_name', 'email')
        return JsonResponse(list(supervisors), safe=False)
    except Group.DoesNotExist:
        return JsonResponse([], safe=False)
    

@never_cache
@require_http_methods('POST')
@login_required
def store(request):
    try:
        leave_data = json.loads(request.body)
        print("Received data:", leave_data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # Process date range BEFORE serializer validation
    leave_date_range = leave_data.get('leave_date_range', '')
    try:
        date_range = leave_date_range.split(" to ")
        from_date, to_date = parse_date(date_range[0]), parse_date(date_range[1]) if len(date_range) > 1 else parse_date(date_range[0])
        if not from_date or not to_date:
            raise ValueError("Invalid date range")
    except (IndexError, ValueError):
        return JsonResponse({'error': 'Invalid leave_date_range format. Expected "YYYY-MM-DD to YYYY-MM-DD".'}, status=422)

    # Add processed dates to the data for serializer validation
    leave_data['from_date'] = from_date.strftime('%Y-%m-%d')
    leave_data['to_date'] = to_date.strftime('%Y-%m-%d')
    
    # Remove the range field as it's not needed by the serializer
    leave_data.pop('leave_date_range', None)

    # Now validate with the serializer
    leave_serializer = LeavesSerializer(data=leave_data)
    if not leave_serializer.is_valid():
        print("Serializer errors:", leave_serializer.errors)
        return JsonResponse(leave_serializer.errors, status=422, safe=False)

    # Continue with overlap check (using the already parsed dates)
    overlapping_leaves = Leaves.objects.filter(
        user_id=request.user.id,
        from_date__lte=to_date,
        to_date__gte=from_date,
    ).exclude(status__in=['REJECTED', 'CANCELLED'])

    if overlapping_leaves.exists():
        return JsonResponse({'error': 'You already have leaves either pending or approved for the applied dates.'}, status=422)

    try:
        leave_type = LeavesTypes.objects.get(id=leave_data['leave_type_id'])
    except LeavesTypes.DoesNotExist:
        return JsonResponse({'error': 'Invalid leave type provided.'}, status=422)

    total_leaves_taken = Leaves.objects.filter(
        user_id=request.user.id, 
        leave_type=leave_type, 
        status='APPROVED'
    ).count()

    if total_leaves_taken >= leave_type.days:
        return JsonResponse({'error': f'You cannot apply for more {leave_type.name} leave than you have been allotted.'}, status=422)

    # Get selected supervisor
    supervisor = None
    if leave_data.get('supervisor_id'):
        try:
            supervisor = User.objects.get(id=leave_data['supervisor_id'])
            # Verify that the selected user is actually a supervisor
            if not supervisor.groups.filter(name='supervisor').exists():
                return JsonResponse({'error': 'Selected user is not a supervisor.'}, status=422)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Selected supervisor not found.'}, status=422)
    else:
        # Fallback to first supervisor if none selected
        try:
            supervisor_group = Group.objects.get(name='supervisor')
            supervisor = User.objects.filter(groups=supervisor_group).first()
        except Group.DoesNotExist:
            pass

    leave_record = Leaves.objects.create(
        user=request.user,
        leave_type=leave_type,
        from_date=from_date,
        to_date=to_date,
        reason=leave_data['reason'],
        supervisor=supervisor,
        status='PENDING_SUPERVISOR'
    )

    # # Send email notification to supervisor
    # if supervisor and supervisor.email :
    #     subject = f'Leave Application for Review - {request.user.get_full_name() or request.user.username}'
        
    #     html_message = render_to_string('emails/leave_application.html', {
    #         'supervisor_name': supervisor.get_full_name() or supervisor.username,
    #         'employee_name': request.user.get_full_name() or request.user.username,
    #         'employee_email': request.user.email,
    #         'leave_type': leave_type.name,
    #         'from_date': from_date.strftime('%B %d, %Y'),
    #         'to_date': to_date.strftime('%B %d, %Y'),
    #         'duration': (to_date - from_date).days + 1,
    #         'reason': leave_data['reason'],
    #     })
        
    #     plain_message = strip_tags(html_message)
        
    #     try:
    #         send_mail(
    #             subject,
    #             plain_message,
    #             settings.DEFAULT_FROM_EMAIL,
    #             [supervisor.email],
    #             fail_silently=False,
    #             html_message=html_message,
    #         )
    #     except Exception as e:
    #         print(f"Failed to send email notification: {e}")
    
    return JsonResponse({'success': 'Leave applied successfully.', 'leave_id': leave_record.id}, status=201)

@never_cache
def all(request):
    body = json.loads(request.body)
    leaves = None
    
    if body['range'] != "":
        range = dateMaker(body['range'])
        if range[0] and range[1]:
            if request.user.is_superuser:
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(created_at__date__range=[range[0],range[1]]).order_by('-id')
            elif request.user.groups.filter(name='supervisor').exists():
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(supervisor=request.user, created_at__date__range=[range[0],range[1]]).order_by('-id')
            else:
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(user_id=request.user.id, created_at__date__range=[range[0],range[1]]).order_by('-id')
        else:
            if request.user.is_superuser:
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(created_at__date=range[0]).order_by('-id')
            elif request.user.groups.filter(name='supervisor').exists():
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(supervisor=request.user, created_at__date=range[0]).order_by('-id')
            else:
                leaves = Leaves.objects.select_related('leave_type', 'user').filter(user_id=request.user.id,created_at__date=range[0]).order_by('-id')
    else:
        if request.user.is_superuser:
            leaves = Leaves.objects.select_related('leave_type', 'user').order_by('-id')
        elif request.user.groups.filter(name='supervisor').exists():
            leaves = Leaves.objects.select_related('leave_type', 'user').filter(supervisor=request.user).order_by('-id')
        else:
            leaves = Leaves.objects.select_related('leave_type', 'user').filter(user=request.user).order_by('-id')

    if body['status'] != "all":
        leaves = leaves.filter(status=body['status'])
    
    paginated_data = make_serialized_pagination(request, leaves, LeavesSerializer)
    return JsonResponse(paginated_data, safe=False)

@login_required
def updateStatus(request, leave_id):
    try:
        leave_obj = Leaves.objects.get(pk=leave_id)
        leave_data = json.loads(request.body)
        new_status = leave_data['status']
        comment = leave_data.get('comment', '')
        
        print(f"DEBUG: Leave ID: {leave_id}")
        print(f"DEBUG: Current status: {leave_obj.status}")
        print(f"DEBUG: New status requested: {new_status}")
        print(f"DEBUG: User: {request.user}")
        print(f"DEBUG: User is supervisor: {request.user.groups.filter(name='supervisor').exists()}")
        print(f"DEBUG: Leave supervisor: {leave_obj.supervisor}")
        print(f"DEBUG: Comment: {comment}")
        
        # Check permissions
        if request.user.groups.filter(name='supervisor').exists():
            # Supervisor can only update leaves they supervise and are pending supervisor approval
            if leave_obj.supervisor != request.user:
                print(f"DEBUG: Supervisor mismatch - leave supervisor: {leave_obj.supervisor}, current user: {request.user}")
                return JsonResponse({'error': 'You can only update leaves assigned to you.'}, status=403)
            
            if leave_obj.status != 'PENDING_SUPERVISOR':
                print(f"DEBUG: Status mismatch - current status: {leave_obj.status}, expected: PENDING_SUPERVISOR")
                return JsonResponse({'error': 'This leave is not pending supervisor approval.'}, status=403)
            
            if new_status == 'APPROVED_BY_SUPERVISOR':
                leave_obj.status = 'PENDING_ADMIN'
                leave_obj.supervisor_comment = comment
                message = 'Leave approved by supervisor'
                print(f"DEBUG: Approving leave - new status: APPROVED")
            elif new_status == 'REJECTED_BY_SUPERVISOR':
                leave_obj.status = 'REJECTED'
                leave_obj.supervisor_comment = comment
                message = 'Leave rejected by supervisor.'
                print(f"DEBUG: Rejecting leave - new status: REJECTED")
                
                # Send email to admin
                admin_users = User.objects.filter(is_superuser=True)
                admin_emails = [admin.email for admin in admin_users if admin.email]
                print(f"DEBUG: Admin emails: {admin_emails}")
                
                if admin_emails and new_status == 'PENDING_ADMIN':
                    subject = f'Leave Application Escalated - {leave_obj.user.get_full_name() or leave_obj.user.username}'
                    
                    # For now, let's skip the HTML email to avoid template errors
                    plain_message = f"""
                    A leave application has been escalated to admin review.
                    
                    Employee: {leave_obj.user.get_full_name() or leave_obj.user.username}
                    Supervisor: {request.user.get_full_name() or request.user.username}
                    Leave Type: {leave_obj.leave_type.name}
                    From: {leave_obj.from_date.strftime('%B %d, %Y')}
                    To: {leave_obj.to_date.strftime('%B %d, %Y')}
                    Reason: {leave_obj.reason}
                    Supervisor Comment: {comment}
                    """
                    
                    try:
                        send_mail(
                            subject,
                            plain_message,
                            settings.DEFAULT_FROM_EMAIL,
                            admin_emails,
                            fail_silently=False,
                        )
                        print(f"DEBUG: Email sent successfully")
                    except Exception as e:
                        print(f"DEBUG: Failed to send email notification: {e}")
            else:
                print(f"DEBUG: Invalid status for supervisor: {new_status}")
                return JsonResponse({'error': 'Invalid status for supervisor'}, status=400)
                
        elif request.user.is_superuser:
            # Admin can update leaves that are pending admin approval
            # if leave_obj.status != 'PENDING_ADMIN':
            #     return JsonResponse({'error': 'This leave is not pending admin approval'}, status=403)
            
            if new_status in ['APPROVED', 'REJECTED']:
                leave_obj.status = new_status
                leave_obj.admin_comment = comment
                message = f'Leave {new_status.lower()} by admin'
            else:
                return JsonResponse({'error': 'Invalid status for admin'}, status=400)
        else:
            return JsonResponse({'error': 'You do not have permission to update this leave status'}, status=403)
        
        # Save the changes
        leave_obj.save()
        print(f"DEBUG: Leave saved with status: {leave_obj.status}")
        
        # Send notification email to employee (simplified)
        if leave_obj.user.email:
            subject = f'Leave Application Status Update - {leave_obj.status.replace("_", " ").title()}'
            
            plain_message = f"""
            Your leave application status has been updated.
            
            Leave Type: {leave_obj.leave_type.name}
            From: {leave_obj.from_date.strftime('%B %d, %Y')}
            To: {leave_obj.to_date.strftime('%B %d, %Y')}
            Status: {leave_obj.status.replace('_', ' ').title()}
            Comment: {comment}
            Updated by: {request.user.get_full_name() or request.user.username}
            """
            
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [leave_obj.user.email],
                    fail_silently=False,
                )
                print(f"DEBUG: Employee notification sent")
            except Exception as e:
                print(f"DEBUG: Failed to send employee notification: {e}")
        
        return JsonResponse({"status": "success", "message": message}, safe=False)
        
    except Leaves.DoesNotExist:
        print(f"DEBUG: Leave not found with ID: {leave_id}")
        return JsonResponse({'error': 'Leave not found'}, status=404)
    except Exception as e:
        print(f"DEBUG: Error in updateStatus: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@never_cache
@require_http_methods('PUT')
@login_required
def update(request, leave_id):
    leave = json.loads(request.body)
    dateRange = leave['leave_date_range'].split(" to ")
    
    # Get supervisor if provided
    supervisor = None
    if leave.get('supervisor_id'):
        try:
            supervisor = User.objects.get(id=leave['supervisor_id'])
            if not supervisor.groups.filter(name='supervisor').exists():
                return JsonResponse({'error': 'Selected user is not a supervisor.'}, status=422)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Selected supervisor not found.'}, status=422)
    
    newData = {
        "leave_type_id": leave['leave_type_id'],
        "from_date": dateRange[0],
        "to_date": dateRange[1],
        "reason": leave['reason'],
    }
    
    # Add supervisor if provided
    if supervisor:
        newData['supervisor'] = supervisor
    
    Leaves.objects.filter(pk=leave_id).update(**newData)
    return JsonResponse({"status": "success", "message": "Leave updated successfully"}, safe=False)

# @login_required
# def updateStatus(request, leave_id):
#     leave = json.loads(request.body)
#     Leaves.objects.filter(pk=leave_id).update(status=leave['status'])
#     return JsonResponse({"status": "success", "message": "Status updated successfully"}, safe=False)


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
        "pending_supervisor": 0,
        "pending_admin": 0,
        "approved_by_supervisor": 0,
        "escalated_to_admin": 0,
        "general": {}
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
        
        stats["total_leaves_applied"] = Leaves.objects.order_by('-id').count()
        stats["total_leaves_pending"] = Leaves.objects.filter(
            status__in=['PENDING_SUPERVISOR', 'PENDING_ADMIN']
        ).order_by('-id').count()
        stats["total_leaves_approved"] = Leaves.objects.filter(
            status='APPROVED').order_by('-id').count()
        stats["total_leaves_rejected"] = Leaves.objects.filter(
            status='REJECTED').order_by('-id').count()
        
        # Admin specific stats
        stats["pending_admin"] = Leaves.objects.filter(status='PENDING_ADMIN').count()
        stats["pending_supervisor"] = Leaves.objects.filter(status='PENDING_SUPERVISOR').count()
        
    elif request.user.groups.filter(name='supervisor').exists():
        # Supervisor specific stats
        supervised_leaves = Leaves.objects.filter(supervisor=request.user)
        
        for i, l in enumerate(generalLeaves):
            name = l['name']
            stats['general'][i] = {
                "name": name,
                "approved": supervised_leaves.filter(
                    status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count(),
                "total": l['days']
            }
        
        stats["total_leaves_applied"] = supervised_leaves.order_by('-id').count()
        stats["total_leaves_pending"] = supervised_leaves.filter(
            status='PENDING_SUPERVISOR'
        ).order_by('-id').count()
        stats["total_leaves_approved"] = supervised_leaves.filter(
            status='APPROVED').order_by('-id').count()
        stats["total_leaves_rejected"] = supervised_leaves.filter(
            status='REJECTED').order_by('-id').count()
        
        # Supervisor specific stats
        stats["pending_supervisor"] = supervised_leaves.filter(status='PENDING_SUPERVISOR').count()
        stats["approved_by_supervisor"] = supervised_leaves.filter(status='APPROVED').count()
        stats["escalated_to_admin"] = supervised_leaves.filter(status='PENDING_ADMIN').count()
        
    else:
        # Employee stats
        for i, l in enumerate(generalLeaves):
            name = l['name']
            stats['general'][i] = {
                "name": name,
                "approved": Leaves.objects.filter(user=request.user).filter(
                     status='APPROVED').filter(leave_type_id=l['id']).order_by('-id').count(),
                "total": l['days']
            }
        
        stats["total_leaves_applied"] = Leaves.objects.filter(user=request.user).order_by('-id').count()
        stats["total_leaves_pending"] = Leaves.objects.filter(user=request.user).filter(
            status__in=['PENDING_SUPERVISOR', 'PENDING_ADMIN']
        ).order_by('-id').count()
        stats["total_leaves_approved"] = Leaves.objects.filter(user=request.user).filter(
            status='APPROVED').order_by('-id').count()
        stats["total_leaves_rejected"] = Leaves.objects.filter(user=request.user).filter(
            status='REJECTED').order_by('-id').count()
    
    return JsonResponse(stats, safe=True)