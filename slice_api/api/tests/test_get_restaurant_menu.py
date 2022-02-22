from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestGetRestaurantMeny(APITestCase):
    fixtures = ["fixtures.json"]

    def test_get_restaurant_menu(self):
        response = self.client.get(
            reverse("get-restaurant-menu-list"), {"id": 1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 2)
        dish_id_list = [dish["id"] for dish in response.data]
        self.assertEqual(dish_id_list, [1, 2])
