from __future__ import annotations

import streamlit as st


def render_results(payload: dict) -> None:
    st.subheader("Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Risk Score", f'{payload["overall"]["score"]:.1f}/100')
        st.metric("Overall Grade", payload["overall"]["grade"])
    with col2:
        st.write("Per-risk scores")
        st.json(payload["risk_scores"])

    st.write("Case findings")
    for case in payload["cases"]:
        with st.container(border=True):
            st.markdown(f'**{case["id"]}** - {case["name"]}')
            st.write(f'Risk: `{case["risk"]}` | Severity: `{case["severity"]}` | Status: `{case["status"]}`')
            st.write(f'Flags: `{", ".join(case["flags"]) if case["flags"] else "none"}`')
            st.code(case["response_excerpt"])
