from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAdminUser

from accounts.models import CustomerProfile, CustomUserModel

from .filters import UserFilter
from .serializers import CustomUserSerializer, MainCustomUserSerializer


class UsersListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = MainCustomUserSerializer
    # * djangoFilterBackend must be specified explicitly (despite global setting) as the other 2 would override it
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    #  this will allow to search by url..../?search=4 or /?search=emailaddress
    #  regex field by email -> less restrictive
    search_fields = ["$email", "id"]
    # default ordering setup on the model with id
    ordering_fields = [
        "id",
        "name",
        "surname",
        "customerprofile__items_sold",
        "customerprofile__items_bought",
        "customerprofile__days_in_row",
    ]
    filterset_class = UserFilter

    def get_queryset(self):
        users = (
            CustomUserModel.objects.all()
            .select_related("customerprofile")
            .prefetch_related("user_permissions", "groups")
        )

        return users
