from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="attendanceIndex"),
    path("", views.index, name="index"),
    path("punch", views.punch, name="attendancePunch"),
    path("summary", views.summary, name="attendanceSummary"),
]
