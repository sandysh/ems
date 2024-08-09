from django.urls import path
from project import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='projectIndex'),
    path("all/", views.AllProjectsView.as_view(), name="AllProjects"),
    path("create/", views.ProjectCreateView.as_view(), name="ProjectCreate"),
    path("update/<int:id>/", views.UpdateProjectView.as_view(), name="UpdateProject"),
    path('add-status/<int:id>/', views.AddProjectStatusView.as_view(), name="AddProjectStatus"),
    path('status/<int:id>/', views.ProjectRelatedStatusView.as_view(), name="ProjectRelatedStatus"),
    path('<int:id>/delete/', views.DeleteProjectView.as_view(), name="DeleteProject"),
    path("all-projects/", views.ProjectFetchView.as_view(), name="ProjectFetch"),
]
