"""Global engine context for cross-cutting concerns.

Manages:
- Server time offset (critical for signed requests)
- Future: rate limit state, connection pool references

The global `context` singleton should be used throughout the client
to ensure consistent timestamp calculation across all requests.
"""
import time


class EngineContext:
    """Global context for the Binance client engine.

    Attributes:
        time_offset: Server time minus local time in milliseconds.
                    Added to local time when generating request timestamps.
        _last_sync: Unix timestamp of last time sync.
    """

    __slots__ = ("time_offset", "_last_sync")

    def __init__(self) -> None:
        self.time_offset: int = 0
        self._last_sync: float = 0.0

    def get_timestamp(self) -> int:
        """Get calibrated timestamp in milliseconds.

        All signed requests should use this instead of time.time().
        The offset compensates for clock drift between client and server.

        Returns:
            Current time in milliseconds, adjusted by server offset.
        """
        return int(time.time() * 1000) + self.time_offset

    def update_offset(self, server_time: int) -> None:
        """Update time offset based on server response.

        Should be called:
        - On client initialization
        - After receiving -1021 TimestampError
        - Periodically (e.g., every hour)

        Args:
            server_time: Server time in milliseconds (from /api/v3/time)
        """
        local_time = int(time.time() * 1000)
        self.time_offset = server_time - local_time
        self._last_sync = time.time()

    def needs_sync(self, interval: float = 3600.0) -> bool:
        """Check if time offset needs re-sync.

        Args:
            interval: Sync interval in seconds (default: 1 hour)

        Returns:
            True if last sync was longer ago than interval.
        """
        return time.time() - self._last_sync > interval

    def has_offset(self) -> bool:
        """Check if time offset has been set.

        Used by HTTPClient to skip redundant time sync when a previous
        client has already synchronized with the server.

        Returns:
            True if time offset is non-zero (sync has been performed).
        """
        return self.time_offset != 0


# Global singleton - used by auth.py and http.py
context = EngineContext()
