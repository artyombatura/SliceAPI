from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestLoginAfterSignUp(APITestCase):
    fixtures = ["fixtures.json"]

    def test_login_after_sign_up(self):
        sign_up_data = {
            "username": "artyom2000",
            "first_name": "artyom",
            "last_name": "ivanov",
            "email": "artyom@gmail.com",
            "password": "artyom123",
            "avatar_url": "http://example.com",
        }
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        sign_in_data = {
            "username": "artyom2000",
            "password": "artyom123",
        }
        response = self.client.post(reverse("login"), sign_in_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["user"]["username"], sign_in_data["username"])
