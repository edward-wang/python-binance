"""Tests for _core/auth.py"""
import pytest
from unittest.mock import patch
from binance._core.auth import sign_request, generate_signature


class TestGenerateSignature:
    def test_generates_hex_signature(self):
        params = {"symbol": "BTCUSDT", "side": "BUY", "timestamp": 1234567890}
        secret = "test_secret"
        sig = generate_signature(params, secret)
        # Signature should be 64 character hex string
        assert len(sig) == 64
        assert all(c in "0123456789abcdef" for c in sig)

    def test_same_params_same_signature(self):
        params = {"symbol": "BTCUSDT", "timestamp": 1234567890}
        secret = "test_secret"
        sig1 = generate_signature(params, secret)
        sig2 = generate_signature(params, secret)
        assert sig1 == sig2

    def test_different_params_different_signature(self):
        secret = "test_secret"
        sig1 = generate_signature({"symbol": "BTCUSDT", "timestamp": 1}, secret)
        sig2 = generate_signature({"symbol": "ETHUSDT", "timestamp": 1}, secret)
        assert sig1 != sig2

    def test_params_sorted_for_consistency(self):
        secret = "test_secret"
        # Same params in different order should produce same signature
        sig1 = generate_signature({"b": "2", "a": "1"}, secret)
        sig2 = generate_signature({"a": "1", "b": "2"}, secret)
        assert sig1 == sig2


class TestSignRequest:
    @patch("binance._core.auth.context")
    def test_adds_timestamp(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert "timestamp" in result
        assert result["timestamp"] == 1234567890000

    @patch("binance._core.auth.context")
    def test_adds_signature(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert "signature" in result
        assert len(result["signature"]) == 64

    @patch("binance._core.auth.context")
    def test_preserves_original_params(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT", "side": "BUY"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert result["symbol"] == "BTCUSDT"
        assert result["side"] == "BUY"

    @patch("binance._core.auth.context")
    def test_uses_existing_timestamp_if_provided(self, mock_context):
        mock_context.get_timestamp.return_value = 9999999999999
        params = {"symbol": "BTCUSDT", "timestamp": 1234567890000}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        # Should use provided timestamp, not context
        assert result["timestamp"] == 1234567890000
