from __future__ import annotations

from time import perf_counter

import requests

from src.adapters.base import ProviderAdapter
from src.models import ModelResponse


class GenericHTTPAdapter(ProviderAdapter):
    def __init__(self, api_key: str, endpoint_url: str) -> None:
        self.api_key = api_key
        self.endpoint_url = endpoint_url

    def complete(self, model: str, system_prompt: str, user_prompt: str) -> ModelResponse:
        start = perf_counter()
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        response = requests.post(self.endpoint_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        raw = response.json()
        text = _extract_text(raw)
        return ModelResponse(text=text, raw=raw, latency_ms=self.elapsed_ms(start))


def _extract_text(raw: dict) -> str:
    if "output_text" in raw and isinstance(raw["output_text"], str):
        return raw["output_text"]
    if "choices" in raw and raw["choices"]:
        choice = raw["choices"][0]
        message = choice.get("message", {})
        if isinstance(message, dict):
            return str(message.get("content", ""))
    if "content" in raw and isinstance(raw["content"], str):
        return raw["content"]
    return ""
