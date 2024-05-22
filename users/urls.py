from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login_user,name="login"),
    path("authenticate",views.authenticate_user, name="authenticate"),
    path("", views.index, name="userIndex"),
    path("all", views.all, name="allUsers"),
    path("create", views.create, name="createUser"),
    path("store",views.store, name="storeUser"),
    path("<int:user_id>/delete",views.destroy, name="deleteUser"),
    path("update/<int:user_id>",views.update, name="updateUser"), 
]
