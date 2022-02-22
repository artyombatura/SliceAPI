from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base_auth_api_test_case import BaseAuthAPITestCaseView


class TestCreditCarsViews(BaseAuthAPITestCaseView):
    def test_credit_cards_list(self):
        response = self.client.get(reverse("get-credit-cards-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 2)

    def test_link_credit_card_success(self):
        valid_credit_card_data = {
            "number": "1111111111111116",
            "expiration_date": "11/16",
            "cvv": "116",
        }
        response = self.client.post(
            reverse("link-credit-card-list"), valid_credit_card_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

    def test_link_credit_card_failure(self):
        invalid_credit_card_data = {}
        response = self.client.post(
            reverse("link-credit-card-list"), invalid_credit_card_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )
        self.assertEqual(len(response.data), 3)

    def test_delete_existing_credit_card(self):
        response = self.client.delete(
            reverse("delete-credit-card-detail", kwargs={"pk": 5}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_not_existing_credit_card(self):
        response = self.client.delete(
            reverse("delete-credit-card-detail", kwargs={"pk": 70}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_delete_another_users_credit_card(self):
        response = self.client.delete(
            reverse("delete-credit-card-detail", kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_no_auth_credit_cards_list(self):
        self.client = APIClient()
        response = self.client.get(reverse("get-credit-cards-list"), format="json")
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_no_auth_delete_credit_card(self):
        self.client = APIClient()
        response = self.client.delete(
            reverse("delete-credit-card-detail", kwargs={"pk": 5}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_no_auth_link_credit_card(self):
        self.client = APIClient()
        valid_credit_card_data = {
            "number": "1111111111111116",
            "expiration_date": "11/16",
            "cvv": "116",
        }
        response = self.client.post(
            reverse("link-credit-card-list"), valid_credit_card_data, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
