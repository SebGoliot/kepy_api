from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.shortcuts import get_snowflake_time
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
            id=42, date_created=get_snowflake_time(42), prefix="!", mute_role_id=123
        )

    def test_guilds_post(self):
        """Testing POST on /guilds/"""
        self.client.force_login(self.user)
        request = self.client.post(
            "/guilds/",
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
        request = self.client.get("/guilds/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["id"], 42)
        self.assertNotEqual(content[0]["id"], 123)

    def test_guilds_get_id(self):
        """Testing GET on /guilds/{pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/guilds/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["id"], 42)
        self.assertNotEqual(content["id"], 123)

    def test_guilds_patch(self):
        """Testing PATCH on /guilds/"""
        self.client.force_login(self.user)

        pre_request = self.client.get("/guilds/42/")
        self.assertEqual(pre_request.json()["prefix"], "!")

        patch_request = self.client.patch(
            "/guilds/42/",
            {
                "prefix": "$",
            },
            content_type='application/json'
        )
        self.assertEqual(patch_request.status_code, 201)

        post_request = self.client.get("/guilds/42/")
        self.assertEqual(post_request.json()["prefix"], "$")

    def test_guilds_patch_invalid(self):
        """Testing invalid PATCH on /guilds/"""
        self.client.force_login(self.user)

        patch_request = self.client.patch(
            "/guilds/42/",
            "42",
            content_type='application/json'
        )

        self.assertEqual(patch_request.status_code, 400)
