from django.urls import path

from . import views

urlpatterns = [
    path("",views.auth_check,name="authCheck"),
    path("login/",views.login_user,name="login"),
    path("authenticate",views.authenticate_user, name="authenticate"),
]
