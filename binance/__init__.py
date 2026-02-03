"""Binance Python Wrapper

High-performance, async-only Python wrapper for Binance API.
"""

__version__ = "2.0.0-dev"

# Core infrastructure (new architecture)
# These will be the primary imports going forward

# Exceptions and enums (preserved)
from binance.exceptions import *  # noqa
from binance.enums import *  # noqa

__all__ = [
    "__version__",
]
