from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestGetRestaurants(APITestCase):
    fixtures = ["fixtures.json"]

    def test_get_restaurants(self):
        response = self.client.get(reverse("restaurants-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(len(response.data[0]), 6)
