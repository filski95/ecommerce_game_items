from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomerProfile, CustomUserModel, Subscription


class CustomerProfileInline(admin.StackedInline):
    """Customer profile's model fields visible on the CustomUser tab in admin"""

    model = CustomerProfile


class SubscriptionInline(admin.StackedInline):
    """Subscription model fields visible on the CustomUser tab in admin"""

    model = Subscription
    readonly_fields = ("trial_used",)


class CustomAdminUser(BaseUserAdmin):
    inlines = [CustomerProfileInline, SubscriptionInline]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "email",
        "name",
        "surname",
        "rating",
        "date_of_birth",
        "is_admin",
        "listed_offers_limit",
    )
    list_filter = ("is_admin", "email")
    ordering = ["email"]

    fieldsets = (
        ("Generic", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("date_of_birth",)}),
        ("Permissions", {"fields": ("is_admin", "is_superuser", "is_staff")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "date_of_birth", "password1", "password2", "name", "surname"),
            },
        ),
    )


admin.site.register(CustomUserModel, CustomAdminUser)
admin.site.register(CustomerProfile)
admin.site.register(Subscription)
