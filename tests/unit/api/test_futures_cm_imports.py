"""Test COIN-M futures API package structure."""


def test_futures_cm_package_importable():
    """Test that futures_cm package exists."""
    import binance.api.futures_cm

    assert binance.api.futures_cm.__name__ == "binance.api.futures_cm"


def test_futures_cm_modules_importable():
    """Test that futures_cm modules exist."""
    from binance.api.futures_cm import general, market, trade, account

    assert general is not None
    assert market is not None
    assert trade is not None
    assert account is not None
