"""Streamlit client for the advanced API; no CrewAI logic lives in the UI."""

from __future__ import annotations

import os

import httpx
import streamlit as st

st.set_page_config(page_title="Agentic Harness Workshop", page_icon="🧭", layout="centered")
st.title("Agentic Harness Workshop")
st.caption("A source-backed decision assistant. All company data is fictional; email is always mocked.")

api_url = os.getenv("WORKSHOP_API_URL", "http://localhost:8000").rstrip("/")
api_token = st.text_input("Workshop API token", type="password")
with st.form("decision"):
    customer_id = st.text_input("Customer ID", value="customer-a")
    question = st.text_area("Decision question", value="Should Northstar AI pilot Meridian AI?")
    remember = st.text_input("Customer constraint to remember (optional)")
    request_email = st.checkbox("Request a mock email approval (does not send email)")
    submitted = st.form_submit_button("Analyze")

if submitted:
    try:
        response = httpx.post(
            f"{api_url}/decisions",
            headers={"X-Workshop-API-Token": api_token},
            json={"customer_id": customer_id, "question": question,
                  "remember": remember or None, "request_email": request_email},
            timeout=180,
        )
        response.raise_for_status()
    except httpx.HTTPError as error:
        st.error(f"API request failed: {error}")
    else:
        st.session_state["decision_result"] = response.json()

if result := st.session_state.get("decision_result"):
    st.subheader("Decision")
    st.write(f"Run: `{result['run_id']}` · Status: `{result['status']}`")
    if report := result.get("report"):
        st.write(f"Recommendation: **{report['recommendation']}**")
        st.write(report["rationale"])
        st.subheader("Evidence")
        for item in report["evidence"]:
            st.write(f"`{item['source_id']}` — {item['claim']}")
        st.subheader("Risks and next steps")
        st.write({"risks": report["risks"], "next_steps": report["next_steps"]})
    else:
        st.warning(result["output"])

    if result["status"] == "pending_approval":
        with st.expander("Instructor-only mock approval"):
            approval_token = st.text_input("Approval token", type="password")
            if st.button("Record mock approval"):
                try:
                    approval = httpx.post(
                        f"{api_url}/decisions/{result['run_id']}/approve",
                        headers={"X-Workshop-Approval-Token": approval_token}, timeout=10,
                    )
                    approval.raise_for_status()
                except httpx.HTTPError as error:
                    st.error(f"Approval failed: {error}")
                else:
                    st.success(approval.json()["result"])
