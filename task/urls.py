from django.urls import path
from task import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='TaskIndex'),
    path("all/", views.AllTaskView.as_view(), name="AllTasks"),
    path("create/", views.TaskCreateView.as_view(), name="TaskCreate"),
    path("update/<int:id>/", views.TaskUpdateView.as_view(), name="UpdateTask"),
    path('<int:id>/delete/', views.DeleteTaskView.as_view(), name="DeleteTask"),

    path('tasks/', views.TaskView.as_view(), name='TaskView'),
]
