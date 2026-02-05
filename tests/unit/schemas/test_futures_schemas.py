"""Test futures API schemas."""


def test_futures_schemas_importable():
    """Test that futures schemas can be imported."""
    from binance._schemas.futures import (
        FuturesExchangeInfo,
        FuturesKline,
        FuturesOrder,
        FuturesAccount,
        FuturesAsset,
        FuturesBalance,
        AccountPosition,
        PositionRisk,
        MarkPrice,
        FundingRate,
        LeverageResult,
        FuturesTicker24h,
        FuturesMyTrade,
    )
    assert FuturesExchangeInfo is not None
    assert FuturesKline is not None
    assert FuturesOrder is not None
    assert AccountPosition is not None
