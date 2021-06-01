from api.shortcuts import get_snowflake_time
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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
            id=42, date_created=get_snowflake_time(42), prefix="!", mute_role_id=123
        )
        discorduser = DiscordUser.objects.create(id=123)
        Member.objects.create(user=discorduser, guild=guild)
        Mute.objects.create(
            id=42, guild=guild, user=discorduser, author=discorduser, duration=42
        )

    def test_mutes_post(self):
        """Testing POST on /guilds/{guild_pk}/members/{member_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.post(
            "/guilds/42/members/123/mutes/",
            {"author": 123, "duration": 42},
        )
        content = request.json()

        self.assertEqual(request.status_code, 201)
        self.assertNotEqual(content["unmute_task_id"], "")

    def test_mutes_get(self):
        """Testing GET on /guilds/{guild_pk}/members/{member_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.get("/guilds/42/members/123/mutes/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["user"], 123)
        self.assertNotEqual(content[0]["user"], 999)

    def test_mutes_get_id(self):
        """Testing GET on /guilds/{guild_pk}/members/{member_pk}/mutes/{mute_pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/guilds/42/members/123/mutes/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["user"], 123)
        self.assertNotEqual(content["user"], 999)

    def test_user_mutes_get(self):
        """Testing GET on /users/{user_pk}/mutes/"""
        self.client.force_login(self.user)
        request = self.client.get("/users/123/mutes/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content[0]["user"], 123)
        self.assertNotEqual(content[0]["user"], 999)

    def test_user_mutes_get_id(self):
        """Testing GET on /users/{user_pk}/mutes/{mute_pk}/"""
        self.client.force_login(self.user)
        request = self.client.get("/users/123/mutes/42/")
        content = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(content["user"], 123)
        self.assertNotEqual(content["user"], 999)

    def test_mutes_cancel(self):
        """Testing cancel on /guilds/{guild_pk}/members/{member_pk}/mutes/{mute_pk}/cancel/"""
        self.client.force_login(self.user)

        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, True)
        self.assertEqual(mute.revoked, False)

        request = self.client.put("/guilds/42/members/123/mutes/42/cancel/")
        self.assertEqual(request.status_code, 204)

        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, False)
        self.assertEqual(mute.revoked, True)

    def test_user_mutes_cancel(self):
        """Testing 403 when cancel on /users/{user_pk}/mutes/{mute_pk}/cancel/"""
        self.client.force_login(self.user)

        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, True)
        self.assertEqual(mute.revoked, False)

        request = self.client.put("/users/123/mutes/42/cancel/")
        self.assertEqual(request.status_code, 403)

        mute = Mute.objects.get(pk=42)
        self.assertEqual(mute.active, True)
        self.assertEqual(mute.revoked, False)
