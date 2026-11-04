"""
Secure Credential Store for Kraftbeat.

Stores sensitive API credentials (such as HuggingFace tokens) exclusively
using the operating system's native secure keyring backend (e.g. SecretService,
KWallet, Windows Credential Manager, macOS Keychain).

FAIL-CLOSED SECURITY POLICY:
If the keyring backend resolves to an unencrypted plaintext file, memory fallback,
or dummy/fail backend, token storage is explicitly refused. No tokens are ever written
to QSettings, config JSON, application logs, or terminal output.
"""

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

SERVICE_NAME = "KraftBeat"
HF_TOKEN_KEY = "huggingface_token"

INSECURE_BACKEND_NAMES = (
    "fail",
    "null",
    "plaintext",
    "file",
    "chainer",
)


def get_keyring_backend():
    """Retrieve active keyring backend, or None if keyring is not installed."""
    try:
        import keyring
        return keyring.get_keyring()
    except Exception as e:
        logger.debug(f"keyring unavailable: {e}")
        return None


def is_secure_keyring_available() -> Tuple[bool, str]:
    """
    Check if a verified secure OS keyring backend is available.
    
    Returns:
        (is_secure: bool, status_message: str)
    """
    backend = get_keyring_backend()
    if backend is None:
        return False, "Keyring package not installed."

    backend_name = backend.__class__.__name__.lower()
    backend_module = getattr(backend, "__module__", "").lower()

    # Reject null/fail/plaintext fallback backends
    for insecure in INSECURE_BACKEND_NAMES:
        if insecure in backend_name or insecure in backend_module:
            return False, f"Insecure or fallback keyring backend detected ({backend.__class__.__name__}). Storage refused."

    return True, f"Secure OS keyring available ({backend.__class__.__name__})."


def store_hf_token(token: str) -> Tuple[bool, str]:
    """
    Store HuggingFace token in OS keyring. Fails closed if backend is not secure.
    
    Args:
        token: User-supplied Hugging Face access token
        
    Returns:
        (success: bool, message: str)
    """
    if not token or not token.strip():
        return False, "Token cannot be empty."

    token = token.strip()
    is_secure, reason = is_secure_keyring_available()
    if not is_secure:
        logger.error(f"Cannot store token: {reason}")
        return False, reason

    try:
        import keyring
        keyring.set_password(SERVICE_NAME, HF_TOKEN_KEY, token)
        logger.info("HuggingFace token securely stored in OS keyring.")
        return True, "HuggingFace token securely stored."
    except Exception as e:
        logger.error(f"Failed to write to OS keyring: {e}")
        return False, f"Keyring write error: {e}"


def get_hf_token() -> Optional[str]:
    """
    Retrieve stored HuggingFace token from OS keyring.
    Returns None if missing or if keyring is unavailable.
    """
    is_secure, _ = is_secure_keyring_available()
    if not is_secure:
        return None

    try:
        import keyring
        token = keyring.get_password(SERVICE_NAME, HF_TOKEN_KEY)
        return token if token else None
    except Exception as e:
        logger.debug(f"Failed to read from OS keyring: {e}")
        return None


def delete_hf_token() -> Tuple[bool, str]:
    """
    Delete stored HuggingFace token from OS keyring.
    """
    is_secure, reason = is_secure_keyring_available()
    if not is_secure:
        return False, reason

    try:
        import keyring
        keyring.delete_password(SERVICE_NAME, HF_TOKEN_KEY)
        logger.info("HuggingFace token removed from OS keyring.")
        return True, "Token removed from keyring."
    except Exception as e:
        logger.debug(f"Failed to delete token from OS keyring: {e}")
        return False, f"Keyring delete error: {e}"
