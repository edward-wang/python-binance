"""Test USDT-M futures API package structure."""


def test_futures_um_package_importable():
    """Test that futures_um package exists."""
    import binance.api.futures_um

    assert binance.api.futures_um.__name__ == "binance.api.futures_um"


def test_futures_um_modules_importable():
    """Test that futures_um modules exist."""
    from binance.api.futures_um import general, market, trade, account

    assert general is not None
    assert market is not None
    assert trade is not None
    assert account is not None
