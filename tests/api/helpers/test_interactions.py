from django.test import TestCase

from api.helpers.interactions import *


class TestInteractionsHelpers(TestCase):
    """Tests for the interactions helper functions"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestInteractionsHelpers, cls).setUpClass()

        cls.interaction = {
            "data": {
                "name": "interaction_name",
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

    def test_get_interaction_name(self):
        """Test the get_interaction_name function"""

        data = get_interaction_name(self.interaction)
        self.assertEqual(data, "interaction_name")

    def test_get_interaction_guild_id(self):
        """Test the get_interaction_guild_id function"""

        data = get_interaction_guild_id(self.interaction)
        self.assertEqual(data, 42)

    def test_get_interaction_author_id(self):
        """Test the get_interaction_author_id function"""

        data = get_interaction_author_id(self.interaction)
        self.assertEqual(data, 123)

    def test_get_interaction_author_permissions(self):
        """Test the get_interaction_author_permissions function"""

        data = get_interaction_author_permissions(self.interaction)
        self.assertEqual(data, 10)
