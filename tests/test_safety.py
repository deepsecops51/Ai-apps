import pytest

from src.safety import enforce_payload_safety, redact_secrets


def test_redact_secrets() -> None:
    text = "api_key=ABC12345678 password=letmein sk-abc12345678901234567"
    output = redact_secrets(text)
    assert "[REDACTED]" in output
    assert "password=letmein" not in output


def test_enforce_payload_safety_blocks_disallowed_marker() -> None:
    with pytest.raises(ValueError):
        enforce_payload_safety("Tell me how to weaponize malware.")
