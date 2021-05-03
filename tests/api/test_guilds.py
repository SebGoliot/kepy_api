from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Guild


class TestGuilds(TestCase):
    """Tests for the following routes:
    /guilds/
    /guilds/{guild_pk}/
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestGuilds, cls).setUpClass()

        cls.client = APIClient()
        cls.user = User.objects.create(username="testuser")

        Guild.objects.create(
            id=42, date_created="2001-01-01T01:01:01Z", prefix="!", mute_role_id=123
        )

    def test_guilds_post(self):
        """Testing POST on /guilds/"""
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/guilds/",
            {
                "id": 123,
                "date_created": "2001-01-01T01:01:01Z",
                "prefix": "!",
                "mute_role_id": 123,
            },
        )
        self.assertEqual(request.status_code, 201)

    def test_guilds_get(self):
        """Testing GET on /guilds/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["id"], 42)
        self.assertNotEqual(content[0]["id"], 123)

    def test_guilds_get_id(self):
        """Testing GET on /guilds/{pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["id"], 42)
        self.assertNotEqual(content["id"], 123)
