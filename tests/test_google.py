from unittest.mock import Mock, patch

import pytest

from jouli.exceptions import LanguageError, ProviderError
from jouli.providers.google import GoogleProvider


@patch("jouli.providers.google.GoogleTranslator")
def test_google_provider_translate_success(mock_translator_class):
    mock_translator = Mock()
    mock_translator.translate.return_value = "Hola"
    mock_translator.detect.return_value = "en"
    mock_translator_class.return_value = mock_translator

    provider = GoogleProvider()
    result = provider.translate("Hello", "es")

    assert result.text == "Hola"
    assert result.source_lang == "en"
    assert result.target_lang == "es"
    assert result.provider == "google"


@patch("jouli.providers.google.GoogleTranslator")
def test_google_provider_detect_language(mock_translator_class):
    mock_translator = Mock()
    mock_translator.detect.return_value = "en"
    mock_translator_class.return_value = mock_translator

    provider = GoogleProvider()
    lang = provider.detect_language("Hello")

    assert lang == "en"


@patch("jouli.providers.google.GoogleTranslator")
def test_google_provider_get_supported_languages(mock_translator_class):
    mock_translator_class.get_supported_languages.return_value = ["en", "es", "fr"]

    provider = GoogleProvider()
    langs = provider.get_supported_languages()

    assert "en" in langs
    assert "es" in langs


@patch("jouli.providers.google.GoogleTranslator")
def test_google_provider_language_not_supported(mock_translator_class):
    from deep_translator.exceptions import LanguageNotSupportedException

    mock_translator = Mock()
    mock_translator.translate.side_effect = LanguageNotSupportedException("xx")
    mock_translator_class.return_value = mock_translator

    provider = GoogleProvider()
    with pytest.raises(LanguageError):
        provider.translate("Hello", "xx")


@patch("jouli.providers.google.GoogleTranslator")
def test_google_provider_request_error(mock_translator_class):
    from deep_translator.exceptions import RequestError

    mock_translator = Mock()
    mock_translator.translate.side_effect = RequestError("Network error")
    mock_translator_class.return_value = mock_translator

    provider = GoogleProvider()
    with pytest.raises(ProviderError):
        provider.translate("Hello", "es")