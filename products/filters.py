import django_filters
from django.forms.widgets import SelectMultiple
from django_filters import rest_framework as dj_filters
from django_filters import widgets

from products.models import Category, Game, Item


def game_choices():
    """
    create a gamelist imitating STATUS_CHOICES usually used in choices arguments
    """
    output = []
    games = Game.objects.all()

    for game in games:
        output.append([game.id, game.game_name])
    return output


def category_choices():
    """
    create a category list imitating STATUS_CHOICES usually used in choices arguments
    """
    output = []
    categories = Category.objects.all()

    for category in categories:
        output.append([category.id, category.category_name])

    return output


class ItemFilter(django_filters.FilterSet):
    game = dj_filters.TypedMultipleChoiceFilter(choices=game_choices)
    category = dj_filters.TypedMultipleChoiceFilter(choices=category_choices)
    # category = dj_filters.ModelMultipleChoiceFilter(field_name="category", queryset=Category.objects.all())
    ingame = dj_filters.BooleanFilter(widget=widgets.BooleanWidget())
    id = dj_filters.Filter(required=False, field_name="id", widget=SelectMultiple(), lookup_expr="in")

    class Meta:
        model = Item
        fields = {
            "name": ["icontains"],
        }


class GameFilter(django_filters.FilterSet):
    age_restriction = dj_filters.NumberFilter()
    age_restriction__lte = dj_filters.NumberFilter(field_name="age_restriction", lookup_expr="lte")
    age_restriction__gte = dj_filters.NumberFilter(field_name="age_restriction", lookup_expr="gte")

    class Meta:
        model = Game
        fields = "__all__"


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        exclude = ["base_hierarchy", "url_slug"]
