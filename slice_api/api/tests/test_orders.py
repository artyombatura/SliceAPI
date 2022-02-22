from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base_auth_api_test_case import BaseAuthAPITestCaseView


class TestOrdersCRUD(BaseAuthAPITestCaseView):
    def test_orders_history(self):
        response = self.client.get(reverse("get-orders-history-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 5)

    def test_create_active_order(self):
        active_order_data = {"restaurant": 6, "dishes": [7, 7, 8]}
        response = self.client.post(
            reverse("create-order-list"), active_order_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        self.assertEqual(response.data["status"], "Active")
        self.assertEqual(len(response.data["dishes"]), 3)

    def test_create_delayed_order(self):
        delayed_order_data = {
            "restaurant": 6,
            "dishes": [7, 7, 8],
            "date": "2023-02-21T14:34:39.553308Z",
        }
        response = self.client.post(
            reverse("create-order-list"), delayed_order_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        self.assertEqual(response.data["status"], "Delayed")
        self.assertEqual(len(response.data["dishes"]), 3)

    def test_create_invalid_order(self):
        invalid_order_data = {"restaurant": 4, "dishes": [7, 7, 8]}
        response = self.client.post(
            reverse("create-order-list"), invalid_order_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_order_update_to_cancelled(self):
        order_update_data = {"status": "Cancelled"}
        response = self.client.put(
            reverse("update-order-detail", kwargs={"pk": 1}),
            order_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["status"], "Cancelled")

    def test_order_update_to_done(self):
        order_update_data = {"status": "Done"}
        response = self.client.put(
            reverse("update-order-detail", kwargs={"pk": 2}),
            order_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["status"], "Done")

    def test_another_users_order_update(self):
        invalid_order_update_data = {"status": "Done"}
        response = self.client.put(
            reverse("update-order-detail", kwargs={"pk": 8}),
            invalid_order_update_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_not_existing_order_update(self):
        invalid_order_update_data = {"status": "Done"}
        response = self.client.put(
            reverse("update-order-detail", kwargs={"pk": 70}),
            invalid_order_update_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_delete_existing_order(self):
        response = self.client.delete(
            reverse("delete-order-detail", kwargs={"pk": 2}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_not_existing_order(self):
        response = self.client.delete(
            reverse("delete-order-detail", kwargs={"pk": 70}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_delete_another_users_order(self):
        response = self.client.delete(
            reverse("delete-order-detail", kwargs={"pk": 8}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_no_auth_create_order(self):
        self.client = APIClient()
        active_order_data = {"restaurant": 6, "dishes": [7, 7, 8]}
        response = self.client.post(
            reverse("create-order-list"), active_order_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_no_auth_order_update(self):
        self.client = APIClient()
        order_update_order_data = {"status": "Cancelled"}
        response = self.client.put(
            reverse("update-order-detail", kwargs={"pk": 1}),
            order_update_order_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_no_auth_delete_order(self):
        self.client = APIClient()
        response = self.client.delete(
            reverse("delete-order-detail", kwargs={"pk": 8}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_no_auth_orders_history(self):
        self.client = APIClient()
        response = self.client.get(reverse("get-orders-history-list"), format="json")
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
