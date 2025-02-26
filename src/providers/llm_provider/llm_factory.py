from src.providers.llm_provider.llm_provider import LLMProvider
from src.providers.llm_provider.ollama_provider import OllamaProvider


class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str) -> LLMProvider:
        if provider_name == "ollama":
            return OllamaProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")