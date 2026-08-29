from unittest.mock import Mock, patch

import pytest

from jouli.core import TranslateEngine
from jouli.exceptions import ProviderError
from jouli.providers import TranslationResult


def test_engine_registers_default_provider():
    engine = TranslateEngine()
    assert "google" in engine.list_providers()


def test_engine_register_provider():
    engine = TranslateEngine()
    mock_provider = Mock()
    mock_provider.name = "mock"
    engine.register_provider(mock_provider)
    assert "mock" in engine.list_providers()


def test_engine_get_provider_not_found():
    engine = TranslateEngine()
    with pytest.raises(ProviderError):
        engine.get_provider("nonexistent")


@patch("jouli.core.GoogleProvider")
def test_translate_calls_provider(mock_google_class):
    mock_provider = Mock()
    mock_provider.translate.return_value = TranslationResult(
        text="Hola",
        source_lang="en",
        target_lang="es",
        provider="google",
    )
    mock_google_class.return_value = mock_provider

    engine = TranslateEngine()
    result = engine.translate("Hello", "es")

    assert result.text == "Hola"
    assert result.target_lang == "es"
    mock_provider.translate.assert_called_once_with("Hello", "es", None)


@patch("jouli.core.GoogleProvider")
def test_detect_language_calls_provider(mock_google_class):
    mock_provider = Mock()
    mock_provider.detect_language.return_value = "en"
    mock_google_class.return_value = mock_provider

    engine = TranslateEngine()
    lang = engine.detect_language("Hello")

    assert lang == "en"
    mock_provider.detect_language.assert_called_once_with("Hello")