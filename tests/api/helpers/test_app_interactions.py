from django.test import TestCase

from api.helpers.app_interactions import *


class TestAppInteractionsHelpers(TestCase):
    """Tests for the mute helper functions"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestAppInteractionsHelpers, cls).setUpClass()

        cls.interaction = {
            "data": {
                "target_id": "123",
                "resolved": {
                    "messages": {
                        "123": {
                            "author": {
                                "id": "42",
                                "username": "test_user",
                            },
                        },
                    },
                },
            },
            "guild_id": "42",
            "member": {
                "permissions": "10",
                "user": {
                    "id": "123",
                },
            },
            "type": 2,
        }

    def test_get_app_message(self):

        data = get_app_message(self.interaction)
        msg = self.interaction["data"]["resolved"]["messages"]["123"]
        self.assertEqual(data, msg)

    def test_get_app_message_author(self):

        data = get_app_message_author(self.interaction)
        author = self.interaction["data"]["resolved"]["messages"]["123"]["author"]
        self.assertEqual(data, author)

    def test_get_app_message_author_id(self):

        data = get_app_message_author_id(self.interaction)
        self.assertEqual(data, "42")

    def test_get_app_message_author_name(self):

        data = get_app_message_author_name(self.interaction)
        self.assertEqual(data, "test_user")
