"""Test that generator dependencies are installed."""


def test_generator_dependencies_importable():
    """Test that generator dependencies are installed."""
    import yaml
    import jinja2

    assert yaml.__version__
    assert jinja2.__version__
