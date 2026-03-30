from __future__ import annotations

from pathlib import Path

import yaml

from src.models import TestCase


def load_cases(path: Path, selected_ids: list[str] | None = None) -> list[TestCase]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    cases = []
    allowed = set(selected_ids or [])
    for item in data.get("cases", []):
        if allowed and item["id"] not in allowed:
            continue
        cases.append(
            TestCase(
                id=item["id"],
                name=item["name"],
                risk=item["risk"],
                severity=int(item["severity"]),
                prompt=item["prompt"],
                expected_secure_behavior=item["expected_secure_behavior"],
                failure_keywords=item.get("failure_keywords", []),
            )
        )
    return cases
