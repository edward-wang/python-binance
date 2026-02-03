"""Tests for _schemas/common.py"""
import msgspec
import pytest
from binance._schemas.common import (
    BaseStruct,
    OrderSide,
    ORDER_SIDE_BUY,
    ORDER_SIDE_SELL,
    OrderType,
    ORDER_TYPE_LIMIT,
    ORDER_TYPE_MARKET,
    TimeInForce,
    TIME_IN_FORCE_GTC,
    Interval,
    INTERVAL_1H,
    INTERVAL_1D,
)


class TestBaseStruct:
    def test_rename_camel(self):
        """Test snake_case to camelCase conversion"""

        class TestStruct(BaseStruct):
            open_time: int
            close_time: int

        # Encode should produce camelCase
        obj = TestStruct(open_time=1, close_time=2)
        encoded = msgspec.json.encode(obj)
        assert b"openTime" in encoded
        assert b"closeTime" in encoded
        assert b"open_time" not in encoded

    def test_decode_from_camel(self):
        """Test decoding camelCase to snake_case"""

        class TestStruct(BaseStruct):
            open_time: int
            close_time: int

        data = b'{"openTime": 1, "closeTime": 2}'
        obj = msgspec.json.decode(data, type=TestStruct)
        assert obj.open_time == 1
        assert obj.close_time == 2

    def test_frozen(self):
        """Test immutability"""

        class TestStruct(BaseStruct):
            value: int

        obj = TestStruct(value=1)
        with pytest.raises(AttributeError):
            obj.value = 2

    def test_omit_defaults(self):
        """Test that None/default fields are omitted"""

        class TestStruct(BaseStruct):
            required: str
            optional: str | None = None

        obj = TestStruct(required="test")
        encoded = msgspec.json.encode(obj)
        assert b"optional" not in encoded


class TestOrderSide:
    def test_buy_constant(self):
        assert ORDER_SIDE_BUY == "BUY"

    def test_sell_constant(self):
        assert ORDER_SIDE_SELL == "SELL"

    def test_type_annotation(self):
        # Should accept valid values
        side: OrderSide = "BUY"
        assert side == "BUY"


class TestOrderType:
    def test_limit_constant(self):
        assert ORDER_TYPE_LIMIT == "LIMIT"

    def test_market_constant(self):
        assert ORDER_TYPE_MARKET == "MARKET"


class TestTimeInForce:
    def test_gtc_constant(self):
        assert TIME_IN_FORCE_GTC == "GTC"


class TestInterval:
    def test_1h_constant(self):
        assert INTERVAL_1H == "1h"

    def test_1d_constant(self):
        assert INTERVAL_1D == "1d"
