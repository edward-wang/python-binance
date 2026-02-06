"""Pre-compiled msgspec decoders for high-frequency endpoints.

Pre-compiled decoders skip type introspection on each call,
providing 20-30% faster decoding for repeated use.

Usage:
    from binance._core.decoders import get_decoder
    from binance._schemas.spot import Kline

    # Get cached decoder (created on first call)
    decoder = get_decoder(list[Kline])

    # Use in hot path
    klines = decoder.decode(raw_bytes)
"""
from typing import Any, TypeVar

import msgspec

T = TypeVar("T")

# Decoder cache - maps type to pre-compiled decoder
_DECODERS: dict[type[Any], msgspec.json.Decoder[Any]] = {}


def get_decoder(schema_type: type[T]) -> msgspec.json.Decoder[T]:
    """Get or create a pre-compiled decoder for the given type.

    The decoder is cached after first creation, so subsequent calls
    with the same type return the same decoder instance.

    Args:
        schema_type: The type to decode into (e.g., Kline, list[Kline])

    Returns:
        A msgspec JSON decoder for the specified type
    """
    if schema_type not in _DECODERS:
        _DECODERS[schema_type] = msgspec.json.Decoder(schema_type)
    return _DECODERS[schema_type]


def clear_decoder_cache() -> None:
    """Clear the decoder cache.

    Primarily useful for testing. In production, decoders should
    remain cached for the lifetime of the application.
    """
    _DECODERS.clear()
