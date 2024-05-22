from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="metricesIndex"),
    path("all", views.all, name="metricesAll"),
    path("store", views.store, name="metricesStore"),
    path("<int:metric_id>/delete", views.destroy, name="metricesDestroy"),
    path("<int:metric_id>/update", views.update, name="metrics.update"),    
]
