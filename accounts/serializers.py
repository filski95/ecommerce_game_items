import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUserModel


class CustomUserSerializer(ModelSerializer):
    """
    this serializer is mostly used by django allauth registration page
    -> password2 added to make sure user typed the password he wanted (comparing both versions)
    since password2 is not on the user model its ditched after the check
    """

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUserModel
        fields = ["email", "password", "password2", "date_of_birth"]

        # to allow dj-rest-registration -> otherwise error with arguments

    def save(self, *args, **kwargs):
        return super().save(**kwargs)

    def validate(self, data):

        password = data.get("password")
        password2 = data.get("password2")

        if password != password2 or not re.search(r"(?=.*[A-Za-z])(?=.*\d)(\w{8,}\d)", password):
            raise serializers.ValidationError(
                "Passwords must match, have at least 8 characters at least 1 number and letter"
            )
        # remove password2 since its not on the user model
        data.pop("password2")

        return data


class MainCustomUserSerializer(ModelSerializer):
    """
    serializer used for list view which will be available to admin only users.
    """

    class Meta:
        model = CustomUserModel
        fields = [
            "id",
            "last_login",
            "email",
            "date_of_birth",
            "name",
            "surname",
            "rating",
            "listed_offers_limit",
            "joined_on",
            "is_superuser",
            "is_active",
            "is_admin",
            "is_staff",
            "groups",
            "user_permissions",
            "customerprofile",
        ]

        # depth set primarily to view attributes of customerprofile. 2 would repeat user which is not desired
        depth = 1
