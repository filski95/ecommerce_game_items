from email.mime import base
from typing import Callable

from django.urls import path, re_path
from rest_framework import routers

from products.views_api import CategoryViewSet, GameViewSet, ItemAttributeViewSet, ItemViewSet

app_name = "products"

router = routers.SimpleRouter()
router.register(r"products/games", GameViewSet, basename="game")
router.register(r"products/categories", CategoryViewSet, basename="category")
router.register(r"products/items", ItemViewSet, basename="item")
router.register(r"products/item_attributes", ItemAttributeViewSet, basename="itemattribute")

# urlpatterns: list[Callable] = []

# urlpatterns += router.urls
