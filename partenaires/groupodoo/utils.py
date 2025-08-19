import hmac
import hashlib


def compute_hmac(secret: str, data: bytes) -> str:
    """Compute HMAC-SHA256 signature."""
    return hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
