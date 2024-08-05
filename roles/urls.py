from django.urls import path, include
from . import views

urlpatterns = [
   
    path('', views.index, name='rolesIndex'),
    path('add/', views.add_role, name='add_role'),
    path('edit/<int:group_id>/', views.edit_role, name='edit_role'),
    path('delete/<int:group_id>/', views.delete_role, name='delete_role'),
    path('<int:group_id>/permission/', views.permissions, name='permissions'),
]