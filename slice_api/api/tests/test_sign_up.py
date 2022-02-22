from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSignUp(APITestCase):
    fixtures = ["fixtures.json"]

    def test_successful_sign_up(self):
        sign_up_data = {
            "username": "alex",
            "first_name": "alex",
            "last_name": "petrov",
            "email": "alex@gmail.com",
            "password": "alex123",
            "avatar_url": "http://example.com",
        }
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

    def test_no_avatar_url_sign_up(self):
        sign_up_data = {
            "username": "alex",
            "first_name": "alex",
            "last_name": "petrov",
            "email": "alex@gmail.com",
            "password": "alex123",
        }
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

    def test_existing_email_sign_up(self):
        sign_up_data = {
            "username": "alex",
            "first_name": "alex",
            "last_name": "petrov",
            "email": "eva@gmail.com",
            "password": "alex123",
        }
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_existing_username_sign_up(self):
        sign_up_data = {
            "username": "eva2000",
            "first_name": "alex",
            "last_name": "petrov",
            "email": "alex@gmail.com",
            "password": "alex123",
        }
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_missing_data_sign_up(self):
        sign_up_data = {}
        response = self.client.post(reverse("signup-list"), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )
        self.assertEqual(len(response.data), 5)
