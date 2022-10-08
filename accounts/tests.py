from datetime import date

from django.test import TestCase
from rest_framework.test import APITestCase

from accounts.models import CustomerProfile, CustomUserModel

# Create your tests here.


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

    def test_customerprofile_automatic_creation(self):
        """customerprofile is created after user is saved -> + linked"""
        profile = self.testuser_1.customerprofile

        self.assertEqual(profile.id, 1)
