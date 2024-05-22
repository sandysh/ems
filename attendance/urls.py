from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="attendanceIndex"),
    path("punch", views.punch, name="attendancePunch"),
    path("summary", views.summary, name="attendanceSummary"),
]
