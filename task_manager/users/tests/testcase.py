from django.test import Client, TestCase

from django.contrib.auth.models import User


class UserTestCase(TestCase):
    fixtures = ["test_users.json"]

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.user_count = User.objects.count()

        self.valid_data = {
            "first_name": "F Name",
            "last_name": "L Name",
            "username": "login1",
            "password1": "ASD123g",  # NOSONAR
            "password2": "ASD123g"  # NOSONAR
        }

        self.update_data = {
            "first_name": "F Name2",
            "last_name": "L Name2",
            "username": "login2",
            "password1": "lpak12",  # NOSONAR
            "password2": "lpak12"  # NOSONAR
        }
