import os
from abc import ABC, abstractmethod


class BaseModelStrategy(ABC):
    name = ""

    @abstractmethod
    def invoke(self, messages):
        raise NotImplementedError


class GroqStrategy(BaseModelStrategy):
    name = "groq"

    def invoke(self, messages):
        from src.common.llm.groq_proxy import invoke_model

        return invoke_model(messages)


class GeminiStrategy(BaseModelStrategy):
    name = "gemini"

    def invoke(self, messages):
        from src.common.llm.gemini_proxy import invoke_model

        return invoke_model(messages)


def get_model_strategy(provider_name=None):
    provider = (provider_name or os.getenv("MODEL_PROVIDER", "groq")).lower()
    strategies = {
        "groq": GroqStrategy(),
        "gemini": GeminiStrategy(),
    }

    try:
        return strategies[provider]
    except KeyError as exc:
        raise ValueError(f"Unsupported model provider: {provider}. Use 'groq' or 'gemini'.") from exc
