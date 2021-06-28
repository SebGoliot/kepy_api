from django.test import TestCase

from discord_perm.discord_perm import (
    check_permissions,
    get_base_permissions,
    get_overwrites,
    has_permission,
)
from discord_perm.discord_perm_const import *


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
            {"roles": ["123"], "user": {"id": "10"}},  # everyone
            {"roles": ["1"], "user": {"id": "11"}},  # admin
            {"roles": ["3"], "user": {"id": "12"}},  # member
            {"roles": ["2", "3"], "user": {"id": "13"}},  # member, moderator
            {"roles": [], "user": {"id": "42"}},  # owner
        ]
        cls.channels = [
            {
                "id": "123",
                "permission_overwrites": [
                    {"id": "123", "allow": "0", "deny": "0"},
                    {"id": "3", "allow": "3197504", "deny": "2176921600"},
                    {"id": "2", "allow": "2176921600", "deny": "0"},
                ],
            },
            {
                "id": "456",
                "permission_overwrites": [
                    {"id": "123", "allow": "0", "deny": "0"},
                    {"id": "12", "allow": "2147553280", "deny": "3146240"},
                ],
            },
            {
                "id": "789",
                "permission_overwrites": [
                    {"id": "123", "allow": "0", "deny": "3072"},
                    {"id": "3", "allow": "3072", "deny": "0"},
                ],
            },
            {
                "id": "789897393889214561",
                "permission_overwrites": [],
            },
        ]

    def test_get_base_permission(self):
        """This test checks if the base permissions are read as they should"""

        # everyone
        permission = get_base_permissions(self.guild, self.members[0])
        # check if those permissions are True
        self.assertTrue(permission & VIEW_CHANNEL == VIEW_CHANNEL)
        self.assertTrue(permission & USE_SLASH_COMMANDS == USE_SLASH_COMMANDS)
        self.assertTrue(permission & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        # check if those permissions are False
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
        self.assertTrue(permission == ALL_PERMISSIONS)

        # owner
        permission = get_base_permissions(self.guild, self.members[4])
        self.assertTrue(permission & ALL_PERMISSIONS == ALL_PERMISSIONS)

        # member
        permission = get_base_permissions(self.guild, self.members[2])
        # check if those permissions are True
        self.assertTrue(permission & SEND_MESSAGES == SEND_MESSAGES)
        self.assertTrue(permission & EMBED_LINKS == EMBED_LINKS)
        self.assertTrue(permission & ATTACH_FILES == ATTACH_FILES)
        self.assertTrue(permission & ADD_REACTIONS == ADD_REACTIONS)
        self.assertTrue(permission & CONNECT == CONNECT)
        self.assertTrue(permission & SPEAK == SPEAK)
        self.assertTrue(permission & STREAM == STREAM)
        # check if those permissions are False
        self.assertFalse(permission & KICK_MEMBERS == KICK_MEMBERS)
        self.assertFalse(permission & BAN_MEMBERS == BAN_MEMBERS)
        self.assertFalse(permission & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertFalse(permission & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertFalse(permission & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertFalse(permission & MOVE_MEMBERS == MOVE_MEMBERS)

        # member & moderator
        permission = get_base_permissions(self.guild, self.members[3])
        # check if those permissions are True
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
        self.assertTrue(permission & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        self.assertTrue(permission & CONNECT == CONNECT)
        self.assertTrue(permission & SPEAK == SPEAK)
        self.assertTrue(permission & STREAM == STREAM)

    def test_get_overwrites(self):
        """This test checks if the permissions overwrites are applied as they
        should
        """

        # member
        permission = get_base_permissions(self.guild, self.members[2])
        overwrites = get_overwrites(
            permission, self.guild["id"], self.members[2], self.channels[0]
        )
        # check if those permissions are now True
        self.assertTrue(overwrites & SEND_MESSAGES == SEND_MESSAGES)
        self.assertTrue(overwrites & EMBED_LINKS == EMBED_LINKS)
        self.assertTrue(overwrites & ATTACH_FILES == ATTACH_FILES)
        self.assertTrue(overwrites & ADD_REACTIONS == ADD_REACTIONS)
        self.assertTrue(overwrites & CONNECT == CONNECT)
        self.assertTrue(overwrites & SPEAK == SPEAK)
        self.assertTrue(overwrites & STREAM == STREAM)
        # check if those permissions are now False
        self.assertFalse(overwrites & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertFalse(overwrites & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        self.assertFalse(overwrites & SEND_TTS_MESSAGES == SEND_TTS_MESSAGES)
        self.assertFalse(overwrites & USE_SLASH_COMMANDS == USE_SLASH_COMMANDS)
        self.assertFalse(overwrites & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertFalse(overwrites & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertFalse(overwrites & MOVE_MEMBERS == MOVE_MEMBERS)

        # moderator
        permission = get_base_permissions(self.guild, self.members[3])
        overwrites = get_overwrites(
            permission, self.guild["id"], self.members[3], self.channels[0]
        )
        # check if those permissions are now True
        self.assertTrue(overwrites & MANAGE_MESSAGES == MANAGE_MESSAGES)
        self.assertTrue(overwrites & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        self.assertTrue(overwrites & SEND_TTS_MESSAGES == SEND_TTS_MESSAGES)
        self.assertTrue(overwrites & USE_SLASH_COMMANDS == USE_SLASH_COMMANDS)
        self.assertTrue(overwrites & MUTE_MEMBERS == MUTE_MEMBERS)
        self.assertTrue(overwrites & DEAFEN_MEMBERS == DEAFEN_MEMBERS)
        self.assertTrue(overwrites & MOVE_MEMBERS == MOVE_MEMBERS)

        # member
        permission = get_base_permissions(self.guild, self.members[2])
        overwrites = get_overwrites(
            permission, self.guild["id"], self.members[2], self.channels[1]
        )
        # check if those permissions are now True
        self.assertTrue(overwrites & READ_MESSAGE_HISTORY == READ_MESSAGE_HISTORY)
        self.assertTrue(overwrites & SEND_TTS_MESSAGES == SEND_TTS_MESSAGES)
        self.assertTrue(overwrites & USE_SLASH_COMMANDS == USE_SLASH_COMMANDS)
        # check if those permissions are now False
        self.assertFalse(overwrites & CONNECT == CONNECT)
        self.assertFalse(overwrites & SPEAK == SPEAK)
        self.assertFalse(overwrites & STREAM == STREAM)

        # admin
        permission = get_base_permissions(self.guild, self.members[1])
        overwrites = get_overwrites(
            permission, self.guild["id"], self.members[1], self.channels[1]
        )
        self.assertTrue(permission & ADMINISTRATOR == ADMINISTRATOR)
        self.assertTrue(permission == ALL_PERMISSIONS)

        # owner
        permission = get_base_permissions(self.guild, self.members[4])
        overwrites = get_overwrites(
            permission, self.guild["id"], self.members[4], self.channels[1]
        )
        permission = get_base_permissions(self.guild, self.members[4])
        self.assertTrue(permission & ALL_PERMISSIONS == ALL_PERMISSIONS)

    def test_check_permission(self):
        """This test checks if the shortcut function behaves as expected
        This test is pretty much the same as the above one
        """

        # member
        # check if those permissions are now True
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[0], SEND_MESSAGES
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[0], EMBED_LINKS
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[0], ATTACH_FILES
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[0], ADD_REACTIONS
            )
        )
        self.assertTrue(
            check_permissions(self.guild, self.members[2], self.channels[0], CONNECT)
        )
        self.assertTrue(
            check_permissions(self.guild, self.members[2], self.channels[0], SPEAK)
        )
        self.assertTrue(
            check_permissions(self.guild, self.members[2], self.channels[0], STREAM)
        )
        # check if those permissions are now False
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], MANAGE_MESSAGES
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], READ_MESSAGE_HISTORY
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], SEND_TTS_MESSAGES
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], USE_SLASH_COMMANDS
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], MUTE_MEMBERS
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], DEAFEN_MEMBERS
            )
        )
        self.assertFalse(
            check_permissions(
                self.guild, self.members[2], self.channels[0], MOVE_MEMBERS
            )
        )

        # moderator
        check_permissions(self.guild, self.members[3], self.channels[0], 0)

        # check if those permissions are now True
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], MANAGE_MESSAGES
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], READ_MESSAGE_HISTORY
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], SEND_TTS_MESSAGES
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], USE_SLASH_COMMANDS
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], MUTE_MEMBERS
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], DEAFEN_MEMBERS
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[3], self.channels[0], MOVE_MEMBERS
            )
        )

        # member
        # check if those permissions are now True
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[1], READ_MESSAGE_HISTORY
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[1], SEND_TTS_MESSAGES
            )
        )
        self.assertTrue(
            check_permissions(
                self.guild, self.members[2], self.channels[1], USE_SLASH_COMMANDS
            )
        )
        # check if those permissions are now False
        self.assertFalse(
            check_permissions(self.guild, self.members[2], self.channels[1], CONNECT)
        )
        self.assertFalse(
            check_permissions(self.guild, self.members[2], self.channels[1], SPEAK)
        )
        self.assertFalse(
            check_permissions(self.guild, self.members[2], self.channels[1], STREAM)
        )


    def test_has_permission(self):
        """This test checks if the shortcut function behaves as expected
        Basically checking if the & operator works..
        """

        self.assertTrue(has_permission(3, 1))   # 00000011 & 00000001
        self.assertTrue(has_permission(3, 2))   # 00000011 & 00000010
