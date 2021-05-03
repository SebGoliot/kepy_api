from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import DiscordUser


class TestUsers(TestCase):
    """Tests for the following routes:
    /users/
    /users/{pk}/
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestUsers, cls).setUpClass()

        cls.client = APIClient()
        cls.user = User.objects.create(username="testuser")

        cls.discorduser = DiscordUser.objects.create(
            id=42,
            username="discord_user",
            discriminator=1234,
            avatar_url="http://test.test/test.png",
            created_at="2001-01-01T01:01:01Z",
        )

    def test_users_post(self):
        """Testing POST on /users/"""
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/users/",
            {
                "id": 123,
                "username": "user",
                "discriminator": 1234,
                "avatar_url": "http://test.test/test.png",
                "created_at": "2001-01-01T01:01:01Z",
            },
        )
        self.assertEqual(request.status_code, 201)

    def test_users_get(self):
        """Testing GET on /users/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/users/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["id"], 42)
        self.assertNotEqual(content[0]["id"], 123)

    def test_users_get_id(self):
        """Testing GET on /users/{pk}"""
        self.client.force_login(self.user)
        request = self.client.get("/api/users/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["id"], 42)
        self.assertNotEqual(content["id"], 123)
