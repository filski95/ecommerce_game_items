from itertools import product

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ErrorDetail, ValidationError


class Game(models.Model):
    MMORPG = "MMORPG"
    RPG = "RPG"
    FPS = "FPS"
    SANDBOX = "SANDBOX"
    GENRE_LIST = [(MMORPG, "MMORPG"), (RPG, "RPG"), (FPS, "FPS"), (SANDBOX, "SANDBOX")]

    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    game_name = models.CharField(max_length=20, unique=True)
    genre = models.CharField(max_length=20, choices=GENRE_LIST)
    release_date = models.DateField()
    age_restriction = models.SmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(18)])

    product_hierarchies = models.ManyToManyField("Category", blank=True)  # only top level - parent = None
    # all categories including top level
    all_product_categories = models.ManyToManyField("Category", blank=True, related_name="games")
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.game_name)

        return super().save(*args, **kwargs)

    def _get_all_subcategories(self, hierarchies, all_categories=None):

        if all_categories is None:
            all_categories = {}

        for category in hierarchies:
            all_categories.update({category: category.hierarchy_identifier})

            # edge case, pass instead of run since we have a list (one "hierarchy leg" might end sooner)
            if not category.child_categories.all():
                pass
            else:
                self._get_all_subcategories(category.child_categories.all(), all_categories)

        return all_categories


class Category(models.Model):
    """
    Hierarchy:
    -> top category (without a parent) determines a base for the hierarchy of the whole structure..
    -> hierarchy structure is simple -> top category starts it with a number say "1" !!ACHTUNG CharField
    -> top parent determines base_hierarchy which is then populated on each child and is subsequently used to create hierarchy_identifier
    -> first child will have "1" + "1" = 11, child of the first child will have "1"+"11" where the first one will be base attrivute
    """

    class Meta:
        verbose_name_plural = "Categories"
        # order: Items (1), Weapons(11)... Reading(2), Books(2)
        ordering = ["base_hierarchy", "hierarchy_identifier"]

    # hierarchy identifier on each depth is constructed of respective nb of concatenations of base
    base_hierarchy = models.CharField(max_length=20, blank=True, null=True, editable=False)
    hierarchy_identifier = models.CharField(max_length=20, blank=True, null=True)
    category_name = models.CharField(max_length=40, unique=True)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_categories"
    )
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    url_slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return self.category_name

    def save(self, *args, **kwargs):
        self._set_base_hierarchy()

        self.url_slug = slugify(self.category_name)

        return super().save(*args, **kwargs)

    def _set_base_hierarchy(self):
        """
        set base category of a child class to the same as its parent, if this is the root (top parent) then make it the same as its identifier
        """
        if self.parent_category is None:
            self.base_hierarchy = self.hierarchy_identifier
        else:
            self.base_hierarchy = self.parent_category.base_hierarchy

    def clean(self) -> None:
        """
        validation for admin purposes
        """

        try:
            int(self.hierarchy_identifier)
        except ValueError:
            raise ValidationError("hierarchy identifier must be integer convertible")


class BaseProduct(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    ingame = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.PositiveSmallIntegerField()
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Item(BaseProduct):
    def __str__(self) -> str:
        return f"{self.name} [{self.id}]"


class ItemAttribute(models.Model):
    # * this is meant to be created by admins in advance

    attribute_name = models.CharField(max_length=50)
    attribute_value = models.CharField(max_length=20, blank=False, null=True)
    attribute_description = models.TextField(blank=True, null=True)
    object = models.ForeignKey(Item, related_name="attributes", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.complete_attribute

    @property
    def complete_attribute(self):
        return self.attribute_name + ": " + self.attribute_value
