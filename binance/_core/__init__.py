"""Core infrastructure for Binance API client.

This package contains hand-written modules that generated code depends on:
- config: URLs and constants
- context: Global engine state (time offset)
- auth: Request signing (HMAC/RSA/Ed25519)
- http: Async HTTP client with connection pooling
- exceptions: Exception hierarchy with error code mapping
- decoders: Pre-compiled msgspec decoders
- formatters: Price/quantity formatting
"""
