"""Have I Been Pwned (HIBP) password breach detection.

Implements k-anonymity protection by only sending the first 5 hex characters
of a SHA-1 hash to the HIBP API, preventing exposure of full password hashes.

See: https://haveibeenpwned.com/API/v3#RangeSearch
"""

import hashlib
import httpx
from typing import Optional

from app.core import config


class HIBPClient:
    def __init__(self, api_url: str = "https://api.pwnedpasswords.com/range/"):
        self.api_url = api_url
        self.client = httpx.Client(timeout=10.0)

    def is_password_compromised(self, password: str) -> bool:
        """Check if password appears in breach database using k-anonymity.

        Args:
            password: The plain-text password to check

        Returns:
            True if the password has been found in a data breach, False otherwise
        """
        if not password or len(password) < 1:
            return False

        # SHA-1 the password (hexadecimal, uppercase) as required by HIBP API
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

        # Split into prefix (first 5 chars) and suffix (rest) for k-anonymity
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        # Query HIBP API for hash range with this prefix
        try:
            response = self.client.get(f"{self.api_url}{prefix}")
            response.raise_for_status()

            # Check if our suffix is in the returned list of suffixes
            # Each line is in format: SUFFIX:COUNT
            return any(line.startswith(f"{suffix}:") for line in response.text.splitlines())
        except Exception:
            # Fail closed - if we can't check, assume not compromised
            # In production, you might want to log this and/or fail open based on policy
            return False

    def close(self):
        """Close the HTTP client."""
        self.client.close()


# Singleton instance for efficiency
_hibp_client: Optional[HIBPClient] = None


def get_hibp_client() -> HIBPClient:
    """Get or create a singleton HIBP client instance."""
    global _hibp_client
    if _hibp_client is None:
        _hibp_client = HIBPClient()
    return _hibp_client


def is_password_compromised(password: str) -> bool:
    """Convenience function to check if a password is compromised.

    Returns False if HIBP is not configured or enabled.
    """
    if not config.is_hibp_configured():
        return False

    client = get_hibp_client()
    try:
        return client.is_password_compromised(password)
    finally:
        # Note: We don't close the singleton here as it's reused
        pass