from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestGetPopularRestaurants(APITestCase):
    fixtures = ["fixtures.json"]

    def test_get_popular_restaurants(self):
        response = self.client.get(
            reverse("get-popular-restaurants-list"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 5)
        popular_restaurant_id_list = [restaurant["id"] for restaurant in response.data]
        self.assertEqual(popular_restaurant_id_list, [4, 5, 2, 3, 6])
