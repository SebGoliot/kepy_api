from django.http import request
from api.views.mute import MuteViewSet
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.request import Request

from api.models import DiscordUser, Guild, Member, Mute


class TestMutes(TestCase):
    """Tests for the following routes:
    /users/{user_pk}/mutes/
    /users/{user_pk}/mutes/{mute_pk}/
    /guilds/{guild_pk}/members/{member_pk}/mutes/
    /guilds/{guild_pk}/members/{member_pk}/mutes/{mute_pk}/
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestMutes, cls).setUpClass()

        cls.client = APIClient()
        cls.user = User.objects.create(username="testuser")

        guild = Guild.objects.create(
            id=42, date_created="2001-01-01T01:01:01Z", prefix="!", mute_role_id=123
        )
        discorduser = DiscordUser.objects.create(
            id=123,
            username="discord_user",
            discriminator=1234,
            avatar_url="http://test.test/test.png",
            created_at="2001-01-01T01:01:01Z",
        )
        Member.objects.create(
            user=discorduser, guild=guild, joined_at="2001-01-01T01:01:01Z"
        )
        cls.mute = Mute.objects.create(
            id=42, guild=guild, user=discorduser, author=discorduser, duration=42
        )

    def test_mutes_post(self):
        """Testing POST on /guilds/{guild_pk}/members/{member_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/guilds/42/members/123/mutes/",
            {"author": 123, "duration": 42},
        )
        content = request.json()

        self.assertEqual(request.status_code, 201)
        self.assertNotEqual(content["unmute_task_id"], "")

    def test_mutes_get(self):
        """Testing GET on /guilds/{guild_pk}/members/{member_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/42/members/123/mutes/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["user"], 123)
        self.assertNotEqual(content[0]["user"], 999)

    def test_mutes_get_id(self):
        """Testing GET on /users/{user_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/42/members/123/mutes/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["user"], 123)
        self.assertNotEqual(content["user"], 999)

    def test_user_mutes_get(self):
        """Testing GET on /users/{user_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/users/123/mutes/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["user"], 123)
        self.assertNotEqual(content[0]["user"], 999)

    def test_user_mutes_get_id(self):
        """Testing GET on /users/{user_pk}/mutes/{mute_pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/users/123/mutes/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["user"], 123)
        self.assertNotEqual(content["user"], 999)
