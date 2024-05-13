from django.urls import path

from .views import user
from .views import metrices
# from .views import ratings

urlpatterns = [
    path("",user.index,name="index"),
    path("login/",user.login_user,name="login"),
    path("authenticate",user.authenticate_user, name="authenticate"),
    path("users/", user.index, name="userIndex"),
    path("users/all", user.all, name="allUsers"),
    path("users/create", user.create, name="createUser"),
    path("users/store",user.store, name="storeUser"),
    path("users/<int:user_id>/delete",user.destroy, name="deleteUser"),
    path("users/update/<int:user_id>",user.update, name="updateUser"),
    path("metrices/", metrices.index, name="metricesIndex"),
    path("metrices/all", metrices.all, name="metricesAll"),
    path("metrices/store", metrices.store, name="metricesStore"),
    path("metrices/<int:metric_id>/delete", metrices.destroy, name="metricesDestroy"),
    path("metrices/<int:metric_id>/update", metrices.update, name="metrics.update"),
    
    # path("ratings/all", ratings.all, name="ratings.all")
]
