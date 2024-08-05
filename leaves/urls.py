from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="leavesIndex"),
     path("store", views.store, name="leavesStore"),
     path("all", views.all, name="leavesAll"),
     path("<int:leave_id>/update", views.update, name="leavesUpdate"),
     path("<int:leave_id>/update/status", views.updateStatus, name="leavesUpdateStatus"),
     path("stats", views.stats, name="leavesStats"),
]