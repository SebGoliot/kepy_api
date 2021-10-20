from django.test import TestCase

from api.helpers.slash_interactions import *


class TestSlashInteractionsHelpers(TestCase):
    """Tests for the slash interactions functions"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestSlashInteractionsHelpers, cls).setUpClass()

        cls.interaction = {
            "data": {
                "options": [
                    {"name": "opt_1", "type": 3, "value": "1"},
                    {"name": "opt_2", "type": 3, "value": "2"},
                ],
            },
            "type": 2,
        }

    def test_get_slash_options(self):

        options = get_slash_options(self.interaction)
        test_data = {
            "opt_1": "1",
            "opt_2": "2",
        }

        self.assertEquals(options, test_data)
