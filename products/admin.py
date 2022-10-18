from django.contrib import admin

from products.models import Category, Game, Item, ItemAttribute

# Register your models here.


class ReverseCategoryInLine(admin.TabularInline):
    model = Category


class AttributeInline(admin.StackedInline):
    model = ItemAttribute


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ReverseCategoryInLine]
    list_display = (
        "category_name",
        "base_hierarchy",
        "hierarchy_identifier",
        "parent_category",
        "created_by",
        "url_slug",
    )

    fieldsets = (
        (
            None,
            {"fields": ("category_name", "hierarchy_identifier", "parent_category", "created_by", "url_slug")},
        ),
    )
    readonly_fields = ["inlines"]


class GameAdmin(admin.ModelAdmin):
    list_display = ["game_name", "genre", "release_date", "age_restriction", "slug"]


class ItemAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]
    list_display = ["name", "description", "ingame", "category", "price", "seller", "game"]


admin.site.register(Game, GameAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAttribute)
