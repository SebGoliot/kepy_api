from api.shortcuts import get_snowflake_time
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import DiscordUser, Guild, Member, Mute


class TestMuteTasks(TestCase):
    """Tests for the following tasks:
    mute
    unmute
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestMuteTasks, cls).setUpClass()

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
