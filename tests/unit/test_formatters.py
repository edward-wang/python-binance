"""Tests for _core/formatters.py"""
import pytest
from binance._core.formatters import format_price, format_quantity, _get_precision


class TestGetPrecision:
    def test_precision_0_01(self):
        assert _get_precision(0.01) == 2

    def test_precision_0_001(self):
        assert _get_precision(0.001) == 3

    def test_precision_0_00001(self):
        assert _get_precision(0.00001) == 5

    def test_precision_1(self):
        assert _get_precision(1.0) == 0

    def test_precision_10(self):
        assert _get_precision(10.0) == 0


class TestFormatPrice:
    def test_format_price_2_decimals(self):
        assert format_price(50000.123456, 0.01) == "50000.12"

    def test_format_price_no_decimals(self):
        assert format_price(50000.99, 1.0) == "50001"

    def test_format_price_rounds_down(self):
        # Python's default rounding, not truncation
        assert format_price(50000.125, 0.01) == "50000.12"

    def test_format_price_rounds_up(self):
        assert format_price(50000.126, 0.01) == "50000.13"


class TestFormatQuantity:
    def test_format_quantity_3_decimals(self):
        assert format_quantity(1.23456789, 0.001) == "1.235"

    def test_format_quantity_5_decimals(self):
        assert format_quantity(0.00123456, 0.00001) == "0.00123"

    def test_format_quantity_no_decimals(self):
        assert format_quantity(100.5, 1.0) == "100"
