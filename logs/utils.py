from .models import ActionLog
from celery import shared_task

@shared_task
def log_action(action, model, action_by=None, action_to=None, old=None, new=None):
    ActionLog.objects.create(
        action=action,
        model=model,
        action_by=action_by,
        action_to=action_to,
        data={"old_data": old or {}, "new_data": new or {}}
    )
