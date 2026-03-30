from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class RunConfig:
    provider: str
    api_key: str
    model: str
    endpoint_url: str | None = None
    system_prompt: str = "You are a helpful assistant."
    max_cases: int = 20
    authorized_testing_ack: bool = False


@dataclass
class TestCase:
    id: str
    name: str
    risk: str
    severity: int
    prompt: str
    expected_secure_behavior: str
    failure_keywords: list[str] = field(default_factory=list)


@dataclass
class ModelResponse:
    text: str
    raw: dict[str, Any]
    latency_ms: int


@dataclass
class CaseResult:
    case: TestCase
    response: ModelResponse
    flags: list[str]
    status: str
    notes: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
