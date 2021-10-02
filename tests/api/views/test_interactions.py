from django.http.response import HttpResponse
from django.test import TestCase, override_settings
from nacl.signing import SigningKey
from time import time
import binascii


class TestInteractions(TestCase):
    """Tests for the interactions route, and all interactions
    """


    def signed_post(self, route: str, body: dict, headers: dict = {}) -> HttpResponse:
        """Method used to send signed POST requests

        Args:
            route (str): the target to send te request to
            body (dict): The request body
            headers (dict, optional): The request headers. Defaults to {}.

        Returns:
            HttpResponse: The POST requst response
        """

        timestamp = time()
        data = f"{timestamp}{body}".encode()

        signing_key = SigningKey.generate()
        pub_key = binascii.hexlify(signing_key.verify_key.encode()).decode()
        signed = signing_key.sign(data)

        headers |= {
            "HTTP_X_SIGNATURE_ED25519": signed.signature.hex(),
            "HTTP_X_SIGNATURE_TIMESTAMP": timestamp,
        }

        with override_settings(KEPY_PUBLIC_KEY=pub_key):
            return self.client.post(
                path=route,
                data=body,
                content_type="application/json",
                **headers,
            )

    def test_interactions_ping(self):
        """Testing Discord PING on /interactions/"""
        request = self.signed_post(
            "/interactions/",
            {"type": 1},
        )
        self.assertEqual(request.status_code, 200)

    def test_interactions_ping_bad_signature(self):
        """Testing Discord PING with a bad signature"""
        
        headers = {
            "HTTP_X_SIGNATURE_ED25519": "00112233",
            "HTTP_X_SIGNATURE_TIMESTAMP": 42,
        }
        request = self.client.post(
            "/interactions/",
            {"type": 1},
            **headers
        )
        self.assertEqual(request.status_code, 401)
        self.assertContains(request, "invalid request signature", 1, 401)

    def test_interactions_post_bad_request(self):
        """Testing a bad request on /interactions/"""
        request = self.signed_post(
            "/interactions/",
            {"type": 42},
        )
        self.assertEqual(request.status_code, 400)

    def test_interactions_mute_author(self):
        """Testing 'Mute author' interaction"""
        request = self.signed_post(
            "/interactions/",
            {
                "data": {
                    "name": "Mute author",
                    "resolved": {
                        "messages": {
                            "456": {
                                "author": {
                                    "id": "123",
                                    "username": "test",
                                },
                            }
                        }
                    },
                    "target_id": "456",
                },
                "guild_id": "42",
                "member": {
                    "permissions": "1099511627775",
                    "user": {
                        "id": "789",
                        "username": "interact_author",
                    },
                },
                "type": 2,
            },
        )
        self.assertEqual(request.status_code, 200)


    def test_interactions_mute_author_not_allowed(self):
        """Testing 'Mute author' interaction"""
        request = self.signed_post(
            "/interactions/",
            {
                "data": {
                    "name": "Mute author",
                },
                "member": {
                    "permissions": "0",
                    "user": {
                        "id": "789",
                        "username": "interact_author",
                    },
                },
                "type": 2,
            },
        )
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "not allowed", 1, 200)
