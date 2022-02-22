from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base_auth_api_test_case import BaseAuthAPITestCaseView


class TestLastVisitedRestaurants(BaseAuthAPITestCaseView):
    def test_last_visited_restaurants(self):
        response = self.client.get(
            reverse("get-last-visited-restaurants-list"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 4)
        popular_restaurant_id_list = [restaurant["id"] for restaurant in response.data]
        self.assertEqual(popular_restaurant_id_list, [4, 3, 2, 1])

    def test_no_auth_credit_cards_list(self):
        self.client = APIClient()
        response = self.client.get(
            reverse("get-last-visited-restaurants-list"), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
