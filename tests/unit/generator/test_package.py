"""Test generator package structure."""


def test_generator_package_importable():
    """Test that generator package structure exists."""
    import generator
    from generator import models, parser, emitter, config

    assert generator.__name__ == "generator"
