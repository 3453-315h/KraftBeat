"""
Unit tests for Fail-Closed Secure Credential Store.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.utils.credentials import (
    is_secure_keyring_available,
    store_hf_token,
    get_hf_token,
    delete_hf_token,
)


class TestCredentials(unittest.TestCase):
    def test_empty_token_refused(self):
        ok, msg = store_hf_token("")
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_fail_closed_on_insecure_backend(self):
        # Create a mock insecure backend
        class PlainTextKeyring:
            pass

        with patch("src.utils.credentials.get_keyring_backend", return_value=PlainTextKeyring()):
            is_secure, reason = is_secure_keyring_available()
            self.assertFalse(is_secure)
            self.assertIn("insecure or fallback", reason.lower())

            # Storing token must be refused
            ok, msg = store_hf_token("hf_test123456789")
            self.assertFalse(ok)
            self.assertIn("refused", msg.lower())

    def test_fail_closed_when_keyring_missing(self):
        with patch("src.utils.credentials.get_keyring_backend", return_value=None):
            is_secure, reason = is_secure_keyring_available()
            self.assertFalse(is_secure)
            self.assertIsNone(get_hf_token())

    def test_secure_storage_success(self):
        class SecretServiceKeyring:
            pass

        mock_backend = SecretServiceKeyring()
        stored_tokens = {}

        def mock_set_password(svc, key, val):
            stored_tokens[(svc, key)] = val

        def mock_get_password(svc, key):
            return stored_tokens.get((svc, key))

        def mock_delete_password(svc, key):
            stored_tokens.pop((svc, key), None)

        with patch("src.utils.credentials.get_keyring_backend", return_value=mock_backend):
            with patch("keyring.set_password", side_effect=mock_set_password):
                with patch("keyring.get_password", side_effect=mock_get_password):
                    with patch("keyring.delete_password", side_effect=mock_delete_password):
                        ok, msg = store_hf_token("hf_valid_token_value")
                        self.assertTrue(ok)

                        tok = get_hf_token()
                        self.assertEqual(tok, "hf_valid_token_value")

                        del_ok, _ = delete_hf_token()
                        self.assertTrue(del_ok)
                        self.assertIsNone(get_hf_token())


if __name__ == '__main__':
    unittest.main()
