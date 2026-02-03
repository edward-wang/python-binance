"""Tests for _core/decoders.py"""
import msgspec
import pytest
from binance._core.decoders import get_decoder, clear_decoder_cache


class SimpleStruct(msgspec.Struct):
    name: str
    value: int


class TestGetDecoder:
    def test_returns_decoder(self):
        decoder = get_decoder(SimpleStruct)
        assert isinstance(decoder, msgspec.json.Decoder)

    def test_decoder_can_decode(self):
        decoder = get_decoder(SimpleStruct)
        result = decoder.decode(b'{"name": "test", "value": 42}')
        assert result.name == "test"
        assert result.value == 42

    def test_caches_decoder(self):
        decoder1 = get_decoder(SimpleStruct)
        decoder2 = get_decoder(SimpleStruct)
        assert decoder1 is decoder2

    def test_different_types_different_decoders(self):
        class OtherStruct(msgspec.Struct):
            data: str

        decoder1 = get_decoder(SimpleStruct)
        decoder2 = get_decoder(OtherStruct)
        assert decoder1 is not decoder2

    def test_list_type(self):
        decoder = get_decoder(list[SimpleStruct])
        result = decoder.decode(b'[{"name": "a", "value": 1}, {"name": "b", "value": 2}]')
        assert len(result) == 2
        assert result[0].name == "a"


class TestClearDecoderCache:
    def test_clear_cache(self):
        decoder1 = get_decoder(SimpleStruct)
        clear_decoder_cache()
        decoder2 = get_decoder(SimpleStruct)
        # After clearing, should create new decoder
        assert decoder1 is not decoder2
