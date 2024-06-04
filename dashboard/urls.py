from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="dashboardIndex"),
    path("stats",views.stats,name="dashboardStats"),
    path("points",views.points,name="dashboardPoints"),
]
