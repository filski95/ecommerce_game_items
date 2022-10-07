from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from accounts.models import CustomUserModel

from .serializers import MainCustomUserSerializer


class UsersListView(ListAPIView):
    serializer_class = MainCustomUserSerializer

    def get_queryset(self):
        users = (
            CustomUserModel.objects.all()
            .select_related("customerprofile")
            .prefetch_related("user_permissions", "groups")
        )

        return users
