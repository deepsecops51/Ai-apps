from __future__ import annotations

import re


DISALLOWED_PAYLOAD_MARKERS = [
    "metasploit",
    "cobalt strike",
    "ransomware",
    "weaponize",
]


def enforce_payload_safety(prompt: str) -> None:
    lowered = prompt.lower()
    for marker in DISALLOWED_PAYLOAD_MARKERS:
        if marker in lowered:
            raise ValueError(f"Blocked potentially dangerous payload marker: {marker}")


def redact_secrets(text: str) -> str:
    patterns = [
        r"sk-[A-Za-z0-9]{16,}",
        r"api[_-]?key\s*[:=]\s*[A-Za-z0-9\-_]{8,}",
        r"password\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
    ]
    redacted = text
    for pattern in patterns:
        redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
    return redacted
