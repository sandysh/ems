from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Leaves
from django.contrib.auth.models import Group


@receiver(post_save, sender=Leaves)
def notify_supervisor_and_admin_on_leave_applied(sender, instance, created, **kwargs):
    if not created:
        return

    leave = instance
    user = leave.user
    duration = (leave.to_date - leave.from_date).days + 1

    print(f"DEBUG: Leave created, sending emails...")
    print(f"DEBUG: Leave ID: {leave.id}, User: {user.username}, Duration: {duration}")

    # 🔹 Send to supervisor(s)
    try:
        supervisors = Group.objects.get(name='supervisor').user_set.all()
        print(f"DEBUG: Found {supervisors.count()} supervisors")
    except Group.DoesNotExist:
        print("DEBUG: Supervisor group does not exist")
        supervisors = []

    if supervisors:
        for supervisor in supervisors:
            if supervisor.email:
                print(f"DEBUG: Sending email to supervisor: {supervisor.email}")
                try:
                    # Prepare email content with supervisor-specific context
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

                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [supervisor.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    print(f"DEBUG: Email sent successfully to {supervisor.email}")
                except Exception as e:
                    print(f"DEBUG: Failed to send email to supervisor {supervisor.email}: {e}")
                    import traceback
                    traceback.print_exc()

    # 🔸 Send to admin(s) if duration > 2
    if duration > 2:
        try:
            admins = Group.objects.get(name='admin').user_set.all()
            print(f"DEBUG: Found {admins.count()} admins for duration > 2")
        except Group.DoesNotExist:
            print("DEBUG: Admin group does not exist")
            admins = []

        if admins:
            for admin in admins:
                if admin.email:
                    print(f"DEBUG: Sending email to admin: {admin.email}")
                    try:
                        # Prepare email content with admin-specific context
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

                        send_mail(
                            subject,
                            plain_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [admin.email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                        print(f"DEBUG: Email sent successfully to admin {admin.email}")
                    except Exception as e:
                        print(f"DEBUG: Failed to send email to admin {admin.email}: {e}")
                        import traceback
                        traceback.print_exc()
    
    print("DEBUG: Email notification process completed")