"""Test that spot API package structure exists."""


def test_api_package_importable():
    """Test that api package exists."""
    import binance.api

    assert binance.api.__name__ == "binance.api"


def test_spot_package_importable():
    """Test that spot package exists."""
    import binance.api.spot

    assert binance.api.spot.__name__ == "binance.api.spot"


def test_spot_submodules_importable():
    """Test that all spot submodules exist."""
    from binance.api.spot import general, market, trade, account

    assert general is not None
    assert market is not None
    assert trade is not None
    assert account is not None
