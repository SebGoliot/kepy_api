from api.shortcuts import get_snowflake_time
from django.test import TestCase

from api.models import DiscordUser, Guild, Member, Mute
from api.helpers.mute import cancel_mute, cancel_member_mutes, end_member_mutes


class TestMuteHelpers(TestCase):
    """Tests for the mute helper functions"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestMuteHelpers, cls).setUpClass()

        guild = Guild.objects.create(
            id=42, date_created=get_snowflake_time(42), prefix="!", mute_role_id=123
        )
        discorduser = DiscordUser.objects.create(id=123)
        Member.objects.create(user=discorduser, guild=guild)
        cls.mute = Mute.objects.create(
            id=42, guild=guild, user=discorduser, author=discorduser, duration=42
        )


    def test_cancel_mute(self):
        """Testing the cancel_mute helper function"""

        self.assertFalse(self.mute.revoked)
        self.assertTrue(self.mute.active)

        cancel_mute(self.mute)
        self.assertTrue(self.mute.revoked)
        self.assertFalse(self.mute.active)


    def test_cancel_member_mutes(self):
        """Testing the cancel_member_mutes helper function"""

        mute = Mute.objects.get(id=self.mute.id)
        self.assertFalse(mute.revoked)
        self.assertTrue(mute.active)

        cancel_member_mutes(42, 123)
        mute = Mute.objects.get(id=self.mute.id)
        self.assertTrue(mute.revoked)
        self.assertFalse(mute.active)

    def test_end_member_mutes(self):
        """Testing the end_member_mutes helper function"""

        mute = Mute.objects.get(id=self.mute.id)
        self.assertFalse(mute.revoked)
        self.assertTrue(mute.active)

        end_member_mutes(42, 123)
        mute = Mute.objects.get(id=self.mute.id)
        self.assertFalse(mute.revoked)
        self.assertFalse(mute.active)
