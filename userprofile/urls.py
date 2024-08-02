from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>", views.profile, name="profile"),
    path('<str:username>/change-password/', views.profile, name='change_password'),
]