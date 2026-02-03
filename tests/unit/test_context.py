"""Tests for _core/context.py"""
import time
import pytest
from binance._core.context import EngineContext, context


def test_engine_context_initial_state():
    ctx = EngineContext()
    assert ctx.time_offset == 0
    assert ctx._last_sync == 0.0


def test_get_timestamp_without_offset():
    ctx = EngineContext()
    before = int(time.time() * 1000)
    ts = ctx.get_timestamp()
    after = int(time.time() * 1000)
    assert before <= ts <= after


def test_get_timestamp_with_offset():
    ctx = EngineContext()
    ctx.time_offset = 1000  # 1 second ahead
    before = int(time.time() * 1000) + 1000
    ts = ctx.get_timestamp()
    after = int(time.time() * 1000) + 1000
    assert before <= ts <= after


def test_update_offset():
    ctx = EngineContext()
    # Simulate server time 500ms ahead
    server_time = int(time.time() * 1000) + 500
    ctx.update_offset(server_time)
    # Offset should be approximately 500ms
    assert 400 <= ctx.time_offset <= 600
    assert ctx._last_sync > 0


def test_needs_sync_initially():
    ctx = EngineContext()
    assert ctx.needs_sync(interval=3600.0) is True


def test_needs_sync_after_update():
    ctx = EngineContext()
    ctx.update_offset(int(time.time() * 1000))
    assert ctx.needs_sync(interval=3600.0) is False


def test_needs_sync_after_interval():
    ctx = EngineContext()
    ctx._last_sync = time.time() - 3700  # 1h 1m 40s ago
    assert ctx.needs_sync(interval=3600.0) is True


def test_global_context_singleton():
    # Global context should be an EngineContext instance
    assert isinstance(context, EngineContext)
