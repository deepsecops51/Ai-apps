from __future__ import annotations

from src.adapters.factory import adapter_from_config
from src.models import CaseResult, RunConfig, TestCase, utc_now_iso
from src.safety import enforce_payload_safety, redact_secrets


def run_suite(config: RunConfig, cases: list[TestCase]) -> dict:
    if not config.authorized_testing_ack:
        raise ValueError("You must acknowledge authorized testing before running.")
    if not config.api_key:
        raise ValueError("API key is required.")

    adapter = adapter_from_config(config)
    selected = cases[: config.max_cases]

    results: list[CaseResult] = []
    for case in selected:
        enforce_payload_safety(case.prompt)
        response = adapter.complete(
            model=config.model,
            system_prompt=config.system_prompt,
            user_prompt=case.prompt,
        )
        safe_text = redact_secrets(response.text)
        response.text = safe_text
        flags = _case_flags(case.failure_keywords, response.text)
        status = "fail" if flags else "pass"
        notes = "Detected risky response markers." if flags else "No risky markers detected."
        results.append(CaseResult(case=case, response=response, flags=flags, status=status, notes=notes))

    return {
        "meta": {
            "generated_at": utc_now_iso(),
            "provider": config.provider,
            "model": config.model,
            "case_count": len(results),
        },
        "results": [case_result_to_dict(r) for r in results],
    }


def _case_flags(keywords: list[str], output: str) -> list[str]:
    lower = output.lower()
    return [kw for kw in keywords if kw.lower() in lower]


def case_result_to_dict(result: CaseResult) -> dict:
    return {
        "id": result.case.id,
        "name": result.case.name,
        "risk": result.case.risk,
        "severity": result.case.severity,
        "status": result.status,
        "flags": result.flags,
        "notes": result.notes,
        "expected_secure_behavior": result.case.expected_secure_behavior,
        "response_text": result.response.text,
        "latency_ms": result.response.latency_ms,
        "raw": result.response.raw,
    }
