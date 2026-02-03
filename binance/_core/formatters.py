"""Price and quantity formatting for order submission.

All calculations use float for HFT performance.
Only format to string at the final order submission step.

Example:
    # Strategy calculation (all float, fast)
    current_price = kline.close  # float
    target_price = current_price * 1.001  # float

    # Only at order submission (format once)
    price_str = format_price(target_price, tick_size=0.01)
    qty_str = format_quantity(0.001234, step_size=0.00001)
"""


def format_price(value: float, tick_size: float) -> str:
    """Format price to match exchange tick size.

    Args:
        value: Price as float
        tick_size: Minimum price increment (e.g., 0.01 for BTCUSDT)

    Returns:
        Price formatted as string with correct precision

    Example:
        format_price(50000.123456, 0.01) → "50000.12"
    """
    precision = _get_precision(tick_size)
    return f"{value:.{precision}f}"


def format_quantity(value: float, step_size: float) -> str:
    """Format quantity to match exchange step size.

    Args:
        value: Quantity as float
        step_size: Minimum quantity increment (e.g., 0.001 for BTCUSDT)

    Returns:
        Quantity formatted as string with correct precision

    Example:
        format_quantity(1.23456789, 0.001) → "1.235"
    """
    precision = _get_precision(step_size)
    return f"{value:.{precision}f}"


def _get_precision(step: float) -> int:
    """Get decimal precision from step size.

    Args:
        step: Step size (tick_size or step_size)

    Returns:
        Number of decimal places
    """
    s = f"{step:.10f}".rstrip("0")
    if "." in s:
        return len(s.split(".")[1])
    return 0
