# OWASP AI Red Team App (Streamlit BYO-API)

This app lets authorized users red-team their own LLM endpoints using OWASP-aligned risk checks.

## Features

- Streamlit UI for setup, attack selection, run, and results.
- Bring-your-own API key for OpenAI, Anthropic, or generic HTTP endpoint.
- OWASP-aligned prompt attack suite:
  - PromptInjection
  - SensitiveDataDisclosure
  - InsecureOutputHandling
  - ExcessiveAgency
  - MisinformationAndUnsafeAdvice
- Per-risk scoring, overall grade, and remediation guidance.
- JSON and Markdown report export.
- Basic safety controls: authorization acknowledgment, payload marker blocking, secret redaction in outputs.

## Quick Start

1. One-command setup:
   - `make setup`
2. Run app:
   - `make run`
3. Open the URL shown by Streamlit (typically `http://localhost:8501`).

## Usage

1. Select provider and model.
2. Enter your API key (never persisted by default).
3. Optionally provide endpoint URL for `generic_http`.
4. Check the authorization acknowledgment.
5. Select OWASP test cases and click **Run Red Team Suite**.
6. Review scores/findings and export reports.

## Run Tests

- `make test`

## Notes

- Use only on systems you own or are explicitly authorized to assess.
- This project is for defensive AI security testing.
