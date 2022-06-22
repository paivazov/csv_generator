from django.contrib.auth.models import User
from django.test import TestCase

from planeks_csv_generator.csv_generator.models import DataSet, DataColumn


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Creating regular active test user
        self.username = "testUser"
        self.user_email = "testUser@mail.com"
        self.user_password = "test"
        user = User.objects.create_user(
            self.username, self.user_email, self.user_password
        )
        self.creds = {"username": "testUser", "password": "test"}

        self.data_set = DataSet.objects.create(name="dataset", user=user)
        self.data_column = DataColumn.objects.create(
            data_set=self.data_set,
            order=4,
            column_name="fff",
            column_type="p_number",
        )
        self.data_column = DataColumn.objects.create(
            data_set=self.data_set,
            order=1,
            column_name="sfasf",
            column_type="p_number",
        )
        self.data_column = DataColumn.objects.create(
            data_set=self.data_set,
            order=4,
            column_name="fasdfafa",
            column_type="p_number",
        )
        self.data_column = DataColumn.objects.create(
            data_set=self.data_set,
            order=3,
            column_name="fasfdasgrg",
            column_type="p_number",
        )

    def test_login_with_valid_credentials_should_be_successful(self):
        """Tests auth/login/ endpoint with correct data"""
        self.client.login(**self.creds)

        response = self.client.get("/datasets/test/1/")

        print(response.status_code)
        # response = self.client.post(
        #     "/datasets/1/schema_column/1/", data={"sklsks": "fklfjl"}
        # )
        # self.assertEqual(response.status_code, 200)
