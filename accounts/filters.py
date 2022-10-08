import django
import django_filters

from .models import CustomUserModel


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUserModel
        fields = {
            "id": ["lt"],
            "rating": ["lt", "gt", "exact"],
            "date_of_birth": ["lt", "gt", "exact"],
            "joined_on": ["lt", "gt", "exact"],
            "is_admin": ["exact"],
            "is_superuser": ["exact"],
            "listed_offers_limit": ["exact"],  # exact makes sense
        }
