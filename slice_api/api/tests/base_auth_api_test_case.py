from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseAuthAPITestCaseView(APITestCase):
    fixtures = ["fixtures.json"]

    def setUp(self):
        sign_in_data = {
            "username": "masha2000",
            "password": "masha",
        }
        response = self.client.post(reverse("login"), sign_in_data, format="json")

        auth_token = response.data["auth_token"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + auth_token)
