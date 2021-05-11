from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.shortcuts import get_snowflake_time
from api.models import DiscordUser, Guild, Member, Mute


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
            id=42, date_created=get_snowflake_time(42), prefix="!", mute_role_id=123
        )
        discorduser = DiscordUser.objects.create(id=42)
        Member.objects.create(user=discorduser, guild=guild)
        Mute.objects.create(
            id=24, guild=guild, user=discorduser, author=discorduser, duration=42
        )
        Mute.objects.create(
            id=42, guild=guild, user=discorduser, author=discorduser, duration=42
        )

    def test_members_post(self):
        """Testing POST on /guilds/{guild_pk}/members/"""
        self.client.force_login(self.user)
        Guild.objects.create(
            id=123, date_created=get_snowflake_time(123), prefix="!", mute_role_id=123
        )
        request = self.client.post(
            "/api/guilds/42/members/",
            {"user": 42, "guild": 123},
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

    def test_cancel_mutes(self):
        """Testing cancel on /guilds/{guild_pk}/members/{member_pk}/cancel-mutes/"""
        self.client.force_login(self.user)

        mute = Mute.objects.get(pk=24)
        self.assertEqual(mute.active, True)
        self.assertEqual(mute.revoked, False)
        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, True)
        self.assertEqual(mute.revoked, False)

        request = self.client.put("/api/guilds/42/members/42/cancel-mutes/")
        self.assertEqual(request.status_code, 204)

        mute = Mute.objects.get(pk=24)
        self.assertEqual(mute.active, False)
        self.assertEqual(mute.revoked, True)
        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, False)
        self.assertEqual(mute.revoked, True)
