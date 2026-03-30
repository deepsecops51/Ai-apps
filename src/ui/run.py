from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml


def _load_case_index() -> list[tuple[str, str]]:
    path = Path("src/tests/owasp_cases.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [(item["id"], f'{item["id"]} - {item["name"]}') for item in data.get("cases", [])]


def render_run_controls() -> tuple[list[str], bool]:
    st.subheader("Attack Suite")
    cases = _load_case_index()
    labels = [label for _, label in cases]
    selected_labels = st.multiselect("Select OWASP-aligned cases", options=labels, default=labels)
    selected_ids = [cid for cid, label in cases if label in selected_labels]
    run_requested = st.button("Run Red Team Suite", type="primary")
    return selected_ids, run_requested
