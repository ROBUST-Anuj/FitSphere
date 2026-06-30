from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="admin@example.com",
            password="Admin@12345",
        )

    def test_login(self):

        url = reverse("accounts:login")

        response = self.client.post(
            url,
            {
                "email": "admin@example.com",
                "password": "Admin@12345",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )
