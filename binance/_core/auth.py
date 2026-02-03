"""Signature generation for Binance API authentication.

Supports HMAC-SHA256 signing. RSA and Ed25519 can be added later.

All signed requests require:
- timestamp: Server-calibrated timestamp in milliseconds
- signature: HMAC-SHA256 of query string using API secret
"""
import hmac
import hashlib
from typing import Any
from urllib.parse import urlencode

from binance._core.context import context


def generate_signature(params: dict[str, Any], secret: str) -> str:
    """Generate HMAC-SHA256 signature for request parameters.

    Args:
        params: Request parameters (will be sorted)
        secret: API secret key

    Returns:
        Hex-encoded signature string (64 characters)
    """
    # Sort params for consistent signature
    query_string = urlencode(sorted(params.items()))
    signature = hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return signature


def sign_request(params: dict[str, Any], secret: str) -> dict[str, Any]:
    """Add timestamp and signature to request params.

    Uses the global context for calibrated timestamp unless
    timestamp is already provided in params.

    Args:
        params: Request parameters (modified in place)
        secret: API secret key

    Returns:
        Parameters with timestamp and signature added
    """
    # Add timestamp if not already present
    if "timestamp" not in params:
        params["timestamp"] = context.get_timestamp()

    # Generate and add signature
    params["signature"] = generate_signature(params, secret)

    return params
