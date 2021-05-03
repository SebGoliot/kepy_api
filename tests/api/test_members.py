from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import DiscordUser, Guild, Member


class TestMembers(TestCase):
    """Tests for the following routes:
    /guilds/{guild_pk}/members/
    /guilds/{guild_pk}/members/{member_pk}/
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestMembers, cls).setUpClass()

        cls.client = APIClient()
        cls.user = User.objects.create(username="testuser")

        guild = Guild.objects.create(
            id=42, date_created="2001-01-01T01:01:01Z", prefix="!", mute_role_id=123
        )
        discorduser = DiscordUser.objects.create(
            id=42,
            username="discord_user",
            discriminator=1234,
            avatar_url="http://test.test/test.png",
            created_at="2001-01-01T01:01:01Z",
        )
        Member.objects.create(
            user=discorduser, guild=guild, joined_at="2001-01-01T01:01:01Z"
        )

    def test_members_post(self):
        """Testing POST on /guilds/{guild_pk}/members/"""
        self.client.force_login(self.user)
        Guild.objects.create(
            id=123, date_created="2001-01-01T01:01:01Z", prefix="!", mute_role_id=123
        )
        request = self.client.post(
            "/api/guilds/42/members/",
            {"user": 42, "guild": 123, "joined_at": "2001-01-01T01:01:01Z"},
        )
        self.assertEqual(request.status_code, 201)

    def test_members_get(self):
        """Testing GET on /guilds/{guild_pk}/members/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/42/members/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["user"], 42)
        self.assertNotEqual(content[0]["user"], 123)

    def test_members_get_id(self):
        """Testing GET on /guilds/{pk}/members/{member_pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/api/guilds/42/members/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["user"], 42)
        self.assertNotEqual(content["user"], 123)
