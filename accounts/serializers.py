import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUserModel


class MyCustomUserSerializer(ModelSerializer):
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

        data.pop("password2")

        return data
