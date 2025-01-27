from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index,name="settingsIndex"),
    path("get_settings", views.get_settings,name="get_settings"),
    path("update_setting/<int:id>", views.update_setting,name="update_setting"),
]
