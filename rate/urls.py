from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="rateIndex"),
    path("store", views.store, name="rateStore"),
    path("latest", views.getLatestRatings, name="rateLatest"),
]
