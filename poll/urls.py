from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='pollIndex'),
    path('get_polls',views.get_polls,name='get_polls'),
    path('set_polls',views.set_polls,name='set_polls'),
]