from django.urls import path

from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("login/",login_user,name="login"),
    path("authenticate",authenticate_user, name="authenticate"),
    path("/", index, name="userIndex"),
    path("all", all, name="allUsers"),
    path("create", create, name="createUser"),
    path("store",store, name="storeUser"),
    path("<int:user_id>/delete",destroy, name="deleteUser"),
    path("update/<int:user_id>",update, name="updateUser"), 
]
