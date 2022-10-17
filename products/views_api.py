from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from products.serializers import CategorySerializer, GameSerializer, ItemAttributeSerializer, ItemSerializer

from .models import Category, Game, Item, ItemAttribute
from .permissions import IsAdminOrReadOnly, IsAdminOrSeller


class GameViewSet(ModelViewSet):

    serializer_class = GameSerializer
    lookup_field = "slug__iexact"
    # * when providing custom case insensitive lookup_field, lookup_url_kwargs default to it unless set otherwise
    # * api/v1/apps/ ^products/games/(?P<game_name__iexact>[^/.]+)/$ [name='game-detail']
    # * this makes drf try to find literally a field "game_name__iexact" which is non existent on the model
    lookup_url_kwarg = "slug"
    # * after lookup_url_kwarg is set to the lookup_field on the serializer
    # * api/v1/apps/ ^products/games/(?P<game_name>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='game-detail']
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        current_user = self.request.user
        if current_user.is_superuser:
            serializer.save(created_by=current_user)
        else:
            raise ValidationError("Currently only admins can create games")

    def get_queryset(self):
        queryset = (
            Game.objects.all()
            .prefetch_related("product_hierarchies", "all_product_categories")
            .select_related("created_by")
        )

        return queryset


class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    # using category names in urls to retrieve objects instead of the default id
    lookup_field = "url_slug__iexact"
    lookup_url_kwarg = "url_slug"

    def perform_create(self, serializer):
        current_user = self.request.user
        if current_user.is_superuser:
            serializer.save(created_by=current_user)
        else:
            raise ValidationError("Currently only admins can create categories")

    def get_queryset(self):

        created_by_parent_category = Category.objects.select_related("created_by", "parent_category")

        queryset = Category.objects.select_related("created_by", "parent_category").prefetch_related(
            Prefetch("child_categories", queryset=created_by_parent_category)
        )

        return queryset

    def get_serializer_context(self):
        standard_context = super().get_serializer_context()

        # explicit info to serializer that this is a list view request
        if self.action == "list":
            standard_context.update({"list_view": True})

        return standard_context


class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAdminOrSeller]
    http_method_names: list[str] = ["put", "post", "get", "options"]

    def get_queryset(self):
        queryset = Item.objects.select_related("seller", "category").prefetch_related("attributes")

        return queryset


class ItemAttributeViewSet(ViewSet):
    def list(self, request):

        queryset = ItemAttribute.objects.all()
        serializer = ItemAttributeSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
