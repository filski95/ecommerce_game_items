from django.urls import path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views_api import UsersListViewSet

app_name = "accounts"
router = SimpleRouter()
router.register("users", UsersListViewSet, basename="users")


urlpatterns = []


urlpatterns += router.urls
