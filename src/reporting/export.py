from __future__ import annotations

import json


def export_json_report(payload: dict) -> str:
    return json.dumps(payload, indent=2)


def export_markdown_report(payload: dict) -> str:
    meta = payload.get("meta", {})
    overall = payload.get("overall", {})
    lines = [
        "# OWASP AI Red Team Report",
        "",
        f'- Provider: `{meta.get("provider", "unknown")}`',
        f'- Model: `{meta.get("model", "unknown")}`',
        f'- Generated At: `{meta.get("generated_at", "unknown")}`',
        f'- Overall Score: `{overall.get("score", 0)}`',
        f'- Grade: `{overall.get("grade", "N/A")}`',
        "",
        "## Risk Scores",
    ]
    for risk, score in payload.get("risk_scores", {}).items():
        lines.append(f"- {risk}: {score}")

    lines.extend(["", "## Top Remediation"])
    for item in payload.get("remediation", [])[:5]:
        lines.append(f'- {item["risk"]} ({item["score"]}): {item["suggestion"]}')

    lines.extend(["", "## Case Results"])
    for case in payload.get("cases", []):
        lines.extend(
            [
                f'- {case["id"]} {case["name"]}',
                f'  - risk: {case["risk"]}',
                f'  - status: {case["status"]}',
                f'  - flags: {", ".join(case["flags"]) if case["flags"] else "none"}',
            ]
        )
    return "\n".join(lines)
