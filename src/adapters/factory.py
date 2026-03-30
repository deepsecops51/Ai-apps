from __future__ import annotations

from src.adapters.anthropic_adapter import AnthropicAdapter
from src.adapters.base import ProviderAdapter
from src.adapters.generic_http_adapter import GenericHTTPAdapter
from src.adapters.openai_adapter import OpenAIAdapter
from src.models import RunConfig


def adapter_from_config(config: RunConfig) -> ProviderAdapter:
    if config.provider == "openai":
        return OpenAIAdapter(api_key=config.api_key)
    if config.provider == "anthropic":
        return AnthropicAdapter(api_key=config.api_key)
    if config.provider == "generic_http":
        if not config.endpoint_url:
            raise ValueError("Generic HTTP provider requires endpoint_url.")
        return GenericHTTPAdapter(api_key=config.api_key, endpoint_url=config.endpoint_url)
    raise ValueError(f"Unsupported provider: {config.provider}")
