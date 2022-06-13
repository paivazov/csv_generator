from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Creating regular active test user
        self.username = "testUser"
        self.user_email = "testUser@mail.com"
        self.user_password = "test"
        User.objects.create_user(
            self.username, self.user_email, self.user_password
        )
        self.creds = {"username": "testUser", "password": "test"}

    def test_login_with_valid_credentials_should_be_successful(self):
        """Tests auth/login/ endpoint with correct data"""
        self.client.login(**self.creds)

        response = self.client.get(reverse("create-dataset-form"))
        print(response.status_code)
