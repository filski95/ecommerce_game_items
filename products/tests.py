from black import assert_equivalent
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models import Category

api_ver = "v1"


class CategoryTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.top_category = Category.objects.create(category_name="Items")

        for i in range(3):
            category = Category.objects.create(category_name=f"Child Item {i}")

    def test_basic_category_list_retrieve(self):
        """
        -> safe methods on category views are generally allowed for all users
        -> lookup_url_kwargs = category_name
        """

        url_detail = reverse(f"{api_ver}:category-detail", kwargs={"url_slug": self.top_category.url_slug})

        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_detail = reverse(f"{api_ver}:category-list")
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.top_category)
        self.assertEqual(len(response.data), Category.objects.count())

    def test_basic_category_detele_view(self):
        url_detail = reverse(f"{api_ver}:category-detail", kwargs={"url_slug": self.top_category.url_slug})

        response = self.client.delete(url_detail)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
