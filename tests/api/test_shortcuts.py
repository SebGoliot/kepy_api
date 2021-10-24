from django.test import TestCase
from datetime import datetime, timezone

from kepy.settings.base import DISCORD_CDN
from api.models import Guild, DiscordUser, Member
from api.shortcuts import *


class TestShortcuts(TestCase):
    """Tests for the api dev shortcuts"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestShortcuts, cls).setUpClass()

        cls.guild = Guild.objects.create(
            id=42, date_created=get_snowflake_time(42), mute_role_id=123
        )
        cls.user = DiscordUser.objects.create(id=42)
        cls.member = Member.objects.create(user=cls.user, guild=cls.guild)


    def test_get_guild_by_id(self):
        """testing get_guild_by_id"""
        
        get_guild = get_guild_by_id(self.guild.id)
        self.assertEqual(get_guild, self.guild)

        new_guild = get_guild_by_id(123)
        self.assertEqual(new_guild.id, 123)


    def test_get_user_by_id(self):
        """testing get_user_by_id"""
        
        get_user = get_user_by_id(self.user.id)
        self.assertEqual(get_user, self.user)

        new_user = get_user_by_id(123)
        self.assertEqual(new_user.id, 123)


    def test_get_member_by_id(self):
        """testing get_member_by_id"""

        g_id = self.guild.id

        get_member = get_member_by_id(g_id, self.user.id)
        self.assertEqual(get_member, self.member)

        new_member = get_member_by_id(g_id, 123)
        self.assertEqual(new_member.user.id, 123)


    def test_get_snowflake_time(self):
        """testing get_snowflake_time"""

        t = get_snowflake_time(42)
        self.assertEqual(t, datetime(2015, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertNotEqual(t, datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc))


    def test_get_avatar_url(self):
        """testing get_avatar_url, wtf am I doing ?!"""
        
        user_id, avatar = 42, 42
        url = f"{DISCORD_CDN}/avatars/{user_id}/{avatar}"

        self.assertEqual(get_avatar_url(42, 42), url)
        self.assertNotEqual(get_avatar_url(123, 42), url)
