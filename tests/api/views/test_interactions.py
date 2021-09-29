from django.test import TestCase

class TestInteractions(TestCase):
    """Tests for the following routes:
    /guilds/
    /guilds/{guild_pk}/
    """

    def test_interactions_ping(self):
        """Testing Discord PING on /interactions/"""
        request = self.client.post(
            "/interactions/",
            {"type": 1},
        )
        self.assertEqual(request.status_code, 200)


    def test_interactions_post_bad_request(self):
        """Testing Discord PING on /interactions/"""
        request = self.client.post(
            "/interactions/",
            {"type": 42},
        )
        self.assertEqual(request.status_code, 400)
