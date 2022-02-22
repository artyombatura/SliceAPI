from django.urls import reverse
from rest_framework import status

from api.tests.base_auth_api_test_case import BaseAuthAPITestCaseView


class TestLogin(BaseAuthAPITestCaseView):
    def test_no_password_login(self):
        sign_in_data = {
            "username": "eva",
        }
        response = self.client.post(reverse("login"), sign_in_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_wrong_password_login(self):
        sign_in_data = {
            "username": "eva2000",
            "password": "alex",
        }
        response = self.client.post(reverse("login"), sign_in_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_no_username_login(self):
        sign_in_data = {
            "password": "evaeva",
        }
        response = self.client.post(reverse("login"), sign_in_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )
