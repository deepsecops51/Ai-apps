from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter

from src.models import ModelResponse


class ProviderAdapter(ABC):
    @abstractmethod
    def complete(self, model: str, system_prompt: str, user_prompt: str) -> ModelResponse:
        raise NotImplementedError

    @staticmethod
    def elapsed_ms(start: float) -> int:
        return int((perf_counter() - start) * 1000)
