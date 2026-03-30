from __future__ import annotations

from time import perf_counter

import anthropic

from src.adapters.base import ProviderAdapter
from src.models import ModelResponse


class AnthropicAdapter(ProviderAdapter):
    def __init__(self, api_key: str) -> None:
        self.client = anthropic.Anthropic(api_key=api_key)

    def complete(self, model: str, system_prompt: str, user_prompt: str) -> ModelResponse:
        start = perf_counter()
        response = self.client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = ""
        if response.content and hasattr(response.content[0], "text"):
            text = response.content[0].text
        raw = response.model_dump()
        return ModelResponse(text=text, raw=raw, latency_ms=self.elapsed_ms(start))
