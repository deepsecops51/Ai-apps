from __future__ import annotations

from time import perf_counter

from openai import OpenAI

from src.adapters.base import ProviderAdapter
from src.models import ModelResponse


class OpenAIAdapter(ProviderAdapter):
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

    def complete(self, model: str, system_prompt: str, user_prompt: str) -> ModelResponse:
        start = perf_counter()
        response = self.client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response.output_text or ""
        raw = response.model_dump()
        return ModelResponse(text=text, raw=raw, latency_ms=self.elapsed_ms(start))
