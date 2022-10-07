from django.urls import path, re_path

from .views_api import UsersListView

app_name = "accounts"

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users_list"),
]
