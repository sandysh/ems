from django.apps import apps
from django.contrib import admin
from logs.models import ActionLog 

admin.site.site_title = "ems"
admin.site.site_header =  "Employee Management System"
admin.site.index_title = "ems"

# Register ActionLog with custom admin before auto-registering everything else
@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model', 'action_by', 'action_to','data', 'timestamp')
    list_filter = ('model', 'action', 'action_by')
    search_fields = ('action', 'model', 'action_by__username', 'action_to__username')
    ordering = ('-timestamp',)

def register_all_app_models():
    """
    Register any unregistered app models. We call this function    after registering any custom     admin classes.
     """
    models_to_ignore = [
        'admin.LogEntry',
        'contenttypes.ContentType',
        'sessions.Session',
        'authtoken.TokenProxy',
        'authtoken.Token',  # We automatically register the authtoken app models.
        'django_celery_beat.PeriodicTask',
        'django_celery_beat.IntervalSchedule',
        'django_celery_beat.CrontabSchedule',
        'django_celery_beat.SolarSchedule',
        'django_celery_beat.ClockedSchedule',
        'django_celery_beat.PeriodicTasks',
    ]
    for model in apps.get_models():
        try:
            if model._meta.label in models_to_ignore:
                continue
            else:
                class modelAdmin(admin.ModelAdmin):
                    list_display = [field.name for field in model._meta.fields]

                admin.site.register(model, modelAdmin)
        except admin.sites.AlreadyRegistered:
            pass


register_all_app_models()
