from email.mime import base
from typing import Callable

from django.urls import path, re_path
from rest_framework import routers

from products.views_api import CategoryViewSet, GameViewSet

app_name = "products"

router = routers.SimpleRouter()
router.register(r"products/games", GameViewSet, basename="game")
router.register(r"products/categories", CategoryViewSet, basename="category")


# urlpatterns: list[Callable] = []

# urlpatterns += router.urls
