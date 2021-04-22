from api.discord_perm.discord_perm_const import *
from api.discord_perm.discord_perm import get_base_permissions
from django.test import TestCase


class TestPermissions(TestCase):
    """Those tests checks the behaviour of the nutella.views methods"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestPermissions, cls).setUpClass()
        cls.guild = {
            "id": "123",
            "owner_id": "42",
            "roles": [
                {
                    "id": "123",
                    "name": "@everyone",
                    "permissions": "2147550208",
                },
                {
                    "id": "1",
                    "name": "admin",
                    "permissions": "8",
                },
                {
                    "id": "2",
                    "name": "modo",
                    "permissions": "29368326",
                },
                {
                    "id": "3",
                    "name": "membre",
                    "permissions": "3197504",
                },
            ],
        }
        cls.members = [
            {
                "roles": ["123"],
                "user": {
                    "id": "1"
                }
            },
            {
                "roles": ["1"],
                "user": {
                    "id": "1"
                }
            },
            {
                "roles": ["3"],
                "user": {
                    "id": "1"
                }
            },
            {
                "roles": ["2", "3"],
                "user": {
                    "id": "1"
                }
            },
        ]

    def test_get_base_permission(self):
        """This test checks if the base permissions are read as they should"""

        #everyone
        permission = get_base_permissions(self.guild, self.members[0])
        # check if those permissions are true
        self.assertTrue(permission & VIEW_CHANNEL == VIEW_CHANNEL)
        self.assertTrue(permission & USE_SLASH_COMMANDS == USE_SLASH_COMMANDS)
        self.assertTrue(
            permission & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        # check if those permissions are false
        self.assertFalse(permission & ADMINISTRATOR == ADMINISTRATOR)
        self.assertFalse(permission & KICK_MEMBERS == KICK_MEMBERS)
        self.assertFalse(permission & BAN_MEMBERS == BAN_MEMBERS)
        self.assertFalse(permission & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertFalse(permission & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertFalse(permission & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertFalse(permission & MOVE_MEMBERS == MOVE_MEMBERS)
        self.assertFalse(permission & SEND_MESSAGES == SEND_MESSAGES)
        self.assertFalse(permission & EMBED_LINKS == EMBED_LINKS)
        self.assertFalse(permission & ATTACH_FILES == ATTACH_FILES)
        self.assertFalse(permission & ADD_REACTIONS == ADD_REACTIONS)
        self.assertFalse(permission & CONNECT == CONNECT)
        self.assertFalse(permission & SPEAK == SPEAK)
        self.assertFalse(permission & STREAM == STREAM)

        # admin
        permission = get_base_permissions(self.guild, self.members[1])
        self.assertTrue(permission & ADMINISTRATOR == ADMINISTRATOR)

        # member
        permission = get_base_permissions(self.guild, self.members[2])
        # check if those permissions are true
        self.assertTrue(permission & SEND_MESSAGES == SEND_MESSAGES)
        self.assertTrue(permission & EMBED_LINKS == EMBED_LINKS)
        self.assertTrue(permission & ATTACH_FILES == ATTACH_FILES)
        self.assertTrue(permission & ADD_REACTIONS == ADD_REACTIONS)
        self.assertTrue(permission & CONNECT == CONNECT)
        self.assertTrue(permission & SPEAK == SPEAK)
        self.assertTrue(permission & STREAM == STREAM)
        # check if those permissions are false
        self.assertFalse(permission & KICK_MEMBERS == KICK_MEMBERS)
        self.assertFalse(permission & BAN_MEMBERS == BAN_MEMBERS)
        self.assertFalse(permission & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertFalse(permission & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertFalse(permission & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertFalse(permission & MOVE_MEMBERS == MOVE_MEMBERS)


        # member & moderator
        permission = get_base_permissions(self.guild, self.members[3])
        self.assertTrue(permission & KICK_MEMBERS == KICK_MEMBERS)
        self.assertTrue(permission & BAN_MEMBERS == BAN_MEMBERS)
        self.assertTrue(permission & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertTrue(permission & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertTrue(permission & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertTrue(permission & MOVE_MEMBERS == MOVE_MEMBERS)
        self.assertTrue(permission & SEND_MESSAGES == SEND_MESSAGES)
        self.assertTrue(permission & EMBED_LINKS == EMBED_LINKS)
        self.assertTrue(permission & ATTACH_FILES == ATTACH_FILES)
        self.assertTrue(permission & ADD_REACTIONS == ADD_REACTIONS)
        self.assertTrue(
            permission & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        self.assertTrue(permission & CONNECT == CONNECT)
        self.assertTrue(permission & SPEAK == SPEAK)
        self.assertTrue(permission & STREAM == STREAM)

