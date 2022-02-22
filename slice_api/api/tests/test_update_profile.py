from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base_auth_api_test_case import BaseAuthAPITestCaseView


class TestUpdateProfile(BaseAuthAPITestCaseView):
    def test_all_fields_profile_update(self):
        profile_update_order_data = {
            "username": "maryia2000",
            "first_name": "maryia",
            "last_name": "ivanova",
            "email": "maryia@gmail.com",
            "password": "maryia",
            "avatar_url": "http://new_example.com",
        }
        response = self.client.put(
            reverse("update-profile-detail", kwargs={"pk": 4}),
            profile_update_order_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["id"], 4)
        self.assertEqual(
            response.data["username"], profile_update_order_data["username"]
        )
        self.assertEqual(
            response.data["first_name"], profile_update_order_data["first_name"]
        )
        self.assertEqual(
            response.data["last_name"], profile_update_order_data["last_name"]
        )
        self.assertEqual(response.data["email"], profile_update_order_data["email"])
        self.assertEqual(
            response.data["avatar_url"], profile_update_order_data["avatar_url"]
        )

    def test_no_fields_profile_update(self):
        profile_update_order_data = {}
        response = self.client.put(
            reverse("update-profile-detail", kwargs={"pk": 4}),
            profile_update_order_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_another_users_profile_update(self):
        profile_update_order_data = {
            "username": "maryia2000",
        }
        response = self.client.put(
            reverse("update-profile-detail", kwargs={"pk": 5}),
            profile_update_order_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_no_auth_profile_update(self):
        self.client = APIClient()
        profile_update_order_data = {
            "username": "maryia2000",
        }
        response = self.client.put(
            reverse("update-profile-detail", kwargs={"pk": 4}),
            profile_update_order_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
