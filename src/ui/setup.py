from __future__ import annotations

import streamlit as st

from src.models import RunConfig


def render_setup() -> RunConfig:
    st.subheader("Setup")
    col1, col2 = st.columns(2)
    with col1:
        provider = st.selectbox("Provider", ["openai", "anthropic", "generic_http"], index=0)
        model = st.text_input("Model", value="gpt-4o-mini")
        api_key = st.text_input("API Key", type="password")
    with col2:
        endpoint_url = st.text_input("Custom endpoint (generic_http only)", value="")
        max_cases = st.number_input("Max cases", min_value=1, max_value=200, value=20, step=1)
        system_prompt = st.text_area("System prompt", value="You are a helpful assistant.")

    authorized = st.checkbox(
        "I confirm I am authorized to test this model endpoint and will use this tool ethically.",
        value=False,
    )

    return RunConfig(
        provider=provider,
        api_key=api_key.strip(),
        model=model.strip(),
        endpoint_url=endpoint_url.strip() or None,
        system_prompt=system_prompt.strip(),
        max_cases=max_cases,
        authorized_testing_ack=authorized,
    )
