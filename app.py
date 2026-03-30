from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from src.engine import run_suite
from src.eval.scorer import score_results
from src.reporting.export import export_markdown_report, export_json_report
from src.tests.loader import load_cases
from src.ui.results import render_results
from src.ui.run import render_run_controls
from src.ui.setup import render_setup


st.set_page_config(page_title="OWASP AI Red Team App", layout="wide")
st.title("OWASP AI Red Team App")
st.caption("Authorized testing only. Run OWASP-aligned red-team checks on your own model endpoints.")

if "last_run_payload" not in st.session_state:
    st.session_state.last_run_payload = None

config = render_setup()
case_selection, run_requested = render_run_controls()

if run_requested:
    cases = load_cases(Path("src/tests/owasp_cases.yaml"), selected_ids=case_selection)
    run_output = run_suite(config=config, cases=cases)
    scored = score_results(run_output)
    st.session_state.last_run_payload = scored

payload = st.session_state.last_run_payload
if payload:
    render_results(payload)
    col1, col2 = st.columns(2)
    with col1:
        json_data = export_json_report(payload)
        st.download_button(
            label="Download JSON Report",
            data=json_data,
            file_name="owasp_redteam_report.json",
            mime="application/json",
        )
    with col2:
        md_data = export_markdown_report(payload)
        st.download_button(
            label="Download Markdown Report",
            data=md_data,
            file_name="owasp_redteam_report.md",
            mime="text/markdown",
        )
else:
    st.info("Configure your provider, select cases, and click Run.")

with st.expander("Raw payload", expanded=False):
    st.code(json.dumps(payload or {}, indent=2), language="json")
