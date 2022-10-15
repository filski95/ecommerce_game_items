from allauth.account.views import ConfirmEmailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from accounts.models import CustomerProfile, CustomUserModel

from .filters import UserFilter
from .permissions import UserOrIsAdmin
from .serializers import CustomUserSerializer, MainCustomUserSerializer


class MyConfirmEmailView(ConfirmEmailView):
    """
    overriden allauth view to use own customized template.
    template is ultimately not used, just

    """

    template_name: str = "accountsasdasd/base.html"


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

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [UserOrIsAdmin]

        return [permission() for permission in permission_classes]
