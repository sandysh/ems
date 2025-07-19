from .models import ActionLog

def log_action(action, model, user=None, target_user=None, old=None, new=None):
    ActionLog.objects.create(
        action=action,
        model=model,
        action_by=user,
        action_to=target_user,
        data={"old_data": old or {}, "new_data": new or {}}
    )
