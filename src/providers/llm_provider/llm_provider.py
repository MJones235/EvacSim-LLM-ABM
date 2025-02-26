from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def call_llm(self, prompt: str, format: str = "json") -> dict | str:
        pass
