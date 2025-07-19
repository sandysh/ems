from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Leaves
from django.contrib.auth.models import Group
from userprofile.models import UserProfile
from .tasks import send_leave_email  # Import the Celery task

# --- Cache old status before save ---
def cache_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Leaves.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Leaves.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

pre_save.connect(cache_old_status, sender=Leaves)

# --- Notify supervisor and admin on leave applied ---
@receiver(post_save, sender=Leaves)
def notify_supervisor_and_admin_on_leave_applied(sender, instance, created, **kwargs):
    if not created:
        return

    leave = instance
    user = leave.user
    duration = (leave.to_date - leave.from_date).days + 1

    # Supervisor notification
    try:
        profile = UserProfile.objects.get(user=user)
        supervisor = profile.supervisor
    except UserProfile.DoesNotExist:
        supervisor = None

    if supervisor and supervisor.email:
        context = {
            'supervisor_name': supervisor.get_full_name() or supervisor.username,
            'employee_name': user.get_full_name() or user.username,
            'employee_email': user.email,
            'leave_type': leave.leave_type.name,
            'from_date': leave.from_date.strftime('%B %d, %Y'),
            'to_date': leave.to_date.strftime('%B %d, %Y'),
            'duration': duration,
            'reason': leave.reason,
        }
        subject = f'Leave Application for Review - {context["employee_name"]}'
        html_message = render_to_string('emails/leave_application.html', context)
        plain_message = strip_tags(html_message)
        send_leave_email.delay(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [supervisor.email],
            html_message
        )

    # Admin notification if duration > 2
    if duration > 2:
        try:
            admins = Group.objects.get(name='admin').user_set.all()
        except Group.DoesNotExist:
            admins = []

        for admin in admins:
            if admin.email:
                context = {
                    'supervisor_name': admin.get_full_name() or admin.username,
                    'employee_name': user.get_full_name() or user.username,
                    'employee_email': user.email,
                    'leave_type': leave.leave_type.name,
                    'from_date': leave.from_date.strftime('%B %d, %Y'),
                    'to_date': leave.to_date.strftime('%B %d, %Y'),
                    'duration': duration,
                    'reason': leave.reason,
                }
                subject = f'Leave Application for Admin Review - {context["employee_name"]}'
                html_message = render_to_string('emails/leave_application.html', context)
                plain_message = strip_tags(html_message)
                send_leave_email.delay(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin.email],
                    html_message
                )

# --- Email to user when they apply for leave (created) ---
@receiver(post_save, sender=Leaves)
def notify_user_on_leave_applied(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user.email:
            context = {
                'employee_name': user.get_full_name() or user.username,
                'leave_type': instance.leave_type.name,
                'from_date': instance.from_date.strftime('%B %d, %Y'),
                'to_date': instance.to_date.strftime('%B %d, %Y'),
                'duration': (instance.to_date - instance.from_date).days + 1,
                'reason': instance.reason,
                'status': instance.status.replace('_', ' ').title(),
            }
            subject = 'Your Leave Application Has Been Submitted'
            html_message = render_to_string('emails/leave_applied_user.html', context)
            plain_message = strip_tags(html_message)
            send_leave_email.delay(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message
            )

# --- Email to user when status changes ---
@receiver(post_save, sender=Leaves)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        user = instance.user
        if user.email:
            context = {
                'employee_name': user.get_full_name() or user.username,
                'leave_type': instance.leave_type.name,
                'from_date': instance.from_date.strftime('%B %d, %Y'),
                'to_date': instance.to_date.strftime('%B %d, %Y'),
                'duration': (instance.to_date - instance.from_date).days + 1,
                'reason': instance.reason,
                'status': instance.status.replace('_', ' ').title(),
            }
            subject = f'Your Leave Application Status Changed to {instance.status.replace("_", " ").title()}'
            html_message = render_to_string('emails/leave_status_changed_user.html', context)
            plain_message = strip_tags(html_message)
            send_leave_email.delay(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message
            )