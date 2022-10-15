from attr import validate
from django.db.models import F
from django.forms import CharField
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from products.models import Category, Game

from .fields import CategoryNameRelatedField


class RecursiveCategorySerializer(serializers.Serializer):
    # https://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects/13377226#13377226
    def to_representation(self, value):

        serializer = self.parent.parent.__class__(value, context=self.context)

        return serializer.data


class CategorySerializer(ModelSerializer):
    # since StringRelatedField is read only I used SlugRelatedField instead, queyrset required for non read only
    parent_category = serializers.SlugRelatedField(
        slug_field="category_name", queryset=Category.objects.all(), allow_null=True
    )
    created_by = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name="category-detail", read_only=True, lookup_field="url_slug")

    # using default reverse relation returns objects with their ids.. SlugRelatedField allows for string desc

    child_categories = RecursiveCategorySerializer(many=True, read_only=True)

    def get_fields(self):
        fields = super().get_fields()

        # do not show recursive relation (tree like structure on the list view as it is fairly expensive)
        # replace it by a SlugSerializer which allows list by a char field
        if self.context.get("list_view"):
            fields["child_categories"] = serializers.SlugRelatedField(
                slug_field="category_name", many=True, read_only=True
            )

        return fields

    class Meta:
        model = Category
        fields = [
            "hierarchy_identifier",
            "category_name",
            "parent_category",
            "created_by",
            "url",
            "child_categories",
        ]

    def validate(self, attrs):
        parent_category = attrs.get("parent_category")
        hierarchy_identifier = attrs.get("hierarchy_identifier")

        # child categories forbid hierarchy_identifier input -> automatic assignment
        if parent_category and hierarchy_identifier:
            raise ValidationError(
                "Reference to a parent category requires hierarchy identifier to be left blank [hierarchy will be determined automatically"
            )

        # top parent category must have hierarchy_identifier + int convertible
        if not parent_category:
            try:
                int(hierarchy_identifier)
            except ValueError:
                raise ValidationError("hierarchy identifier must be integer convertible")

        return attrs

    def create(self, validated_data):
        parent_category = validated_data.get("parent_category")
        # if this is a child category use base_hierarchy of a parent class and concatenate it with already concatenated hierarchy_identifier of a parent class.
        # (this way is always the same as top parent)
        if parent_category is not None:
            parent_hierarchy = parent_category.hierarchy_identifier
            base = parent_category.base_hierarchy

            validated_data["hierarchy_identifier"] = base + parent_hierarchy
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        -> updates hierarchy_identifier and parent_category in case parent_category was changed (validation wont allow both fields - no validation on identifier needed)
        -> updates category_name if provided
        -> purposefully ignores updates of hierarchy_identifier:
        a) for root category it would require recursive update of all sub-categories
        b) for child categories validation wont allow it anyway
        """
        parent_category = validated_data.get("parent_category")

        if parent_category:
            parent_hierarchy = parent_category.hierarchy_identifier
            base_hierarchy = parent_category.base_hierarchy

            instance.hierarchy_identifier = base_hierarchy + parent_hierarchy
            instance.parent_category = parent_category
            instance.save()

        # change category_name if new name was provided
        instance.category_name = validated_data.get("category_name", instance.category_name)

        return instance


class GameSerializer(ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="game-detail", read_only=True, lookup_field="slug")
    created_by = serializers.StringRelatedField()
    all_product_categories = CategoryNameRelatedField(many=True, read_only=True, required=False)
    product_hierarchies = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.filter(hierarchy_identifier=F("base_hierarchy")),
        view_name="category-detail",
        lookup_field="url_slug",
        many=True,
    )

    class Meta:
        model = Game
        fields = [
            "game_name",
            "genre",
            "release_date",
            "age_restriction",
            "created_by",
            "url",
            "product_hierarchies",
            "all_product_categories",
        ]

    def update(self, instance, validated_data):

        request_prod_categories = validated_data.get("product_hierarchies")  # list or None

        if request_prod_categories is None:
            # patch requests without changes in product_categories can skip this part
            pass
        else:
            validated_data["all_product_categories"] = instance._get_all_subcategories(request_prod_categories)

        return super().update(instance, validated_data)

    def create(self, validated_data):

        product_hierarchies = validated_data.pop("product_hierarchies", None)

        new_game = Game.objects.create(**validated_data)

        if product_hierarchies:
            new_game.product_hierarchies.set(product_hierarchies)
            new_game.all_product_categories.set(new_game._get_all_subcategories(product_hierarchies))

        return new_game
