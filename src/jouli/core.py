from jouli.exceptions import ProviderError
from jouli.providers import GoogleProvider, TranslationResult, TranslatorProvider


class TranslateEngine:
    """Core translation engine with provider management."""

    def __init__(self):
        self._providers: dict[str, TranslatorProvider] = {}
        self._register_default_providers()

    def _register_default_providers(self):
        self._providers["google"] = GoogleProvider()

    def register_provider(self, provider: TranslatorProvider):
        self._providers[provider.name] = provider

    def get_provider(self, name: str) -> TranslatorProvider:
        if name not in self._providers:
            raise ProviderError("engine", f"Provider '{name}' not found")
        return self._providers[name]

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: str | None = None,
        provider_name: str = "google",
    ) -> TranslationResult:
        provider = self.get_provider(provider_name)
        return provider.translate(text, target_lang, source_lang)

    def detect_language(self, text: str, provider_name: str = "google") -> str:
        provider = self.get_provider(provider_name)
        return provider.detect_language(text)

    def get_supported_languages(self, provider_name: str = "google") -> list[str]:
        provider = self.get_provider(provider_name)
        return provider.get_supported_languages()

    def list_providers(self) -> list[str]:
        return list(self._providers.keys())


engine = TranslateEngine()