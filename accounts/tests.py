from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomerProfile, CustomUserModel


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.testuser_1 = CustomUserModel.objects.create_user(
            email="test@gmail.com",
            name="test_name",
            surname="test_surname",
            date_of_birth=date(1990, 7, 17),
            password="adminadmin123",
        )

        cls.admin_user = CustomUserModel.objects.create_superuser(
            email="admin@gmail.com",
            name="admin",
            surname="admin_surname",
            date_of_birth=date(1990, 7, 17),
            password="adminadmin123",
        )

    def test_customerprofile_automatic_creation(self):
        """customerprofile is created after user is saved -> + linked"""
        profile = self.testuser_1.customerprofile

        self.assertEqual(profile.id, 1)

    def test_JWT_users_list_view(self):
        """
        testing simple_jwt with users list
        1. obtaining refresh token and access token,
        2. using wrong token and actual access token with the views
        3. using refresh token to get the access again
        """
        jwt_url = reverse("token_obtain_pair")  # url to get token

        response_obtained_tokens = self.client.post(
            jwt_url, {"email": self.admin_user.email, "password": "adminadmin123"}, format="json"
        )

        # accessing token_obtain_pair returns {refresh_token:token, access_token:token} (curl -H)
        refresh_token, access_token = response_obtained_tokens.data.values()

        # use wrong token and get 401 status code
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer fake_token")
        response_bad_req = self.client.get(reverse("accounts:users-list"))
        self.assertEqual(response_bad_req.status_code, status.HTTP_401_UNAUTHORIZED)

        # use correct token and get 200 OK
        # * usage of access token-> in the header: Bearer ACCESS TOKEN
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("accounts:users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # use refresh token and get 200 + new access token
        refresh_url = reverse("token_refresh")
        # * usage of refresh token requries using {"refresh": refresh_token} in the data (curl -d)
        response_refresh_token = self.client.post(refresh_url, data={"refresh": refresh_token})
        self.assertEqual(response_refresh_token.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_refresh_token.data)
