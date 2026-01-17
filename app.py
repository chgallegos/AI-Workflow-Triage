from __future__ import annotations

import json
import uuid
import streamlit as st

from src.schemas import IntakeRequest, TicketRecord
from src.classifier import classify
from src.workflow import route
from src.logger import build_audit_log, audit_event, now_iso

st.set_page_config(page_title="AI Workflow Triage Bot", layout="wide")

st.title("AI Workflow Triage Bot")
st.caption("Demo: classify + route employee ops requests with confidence thresholds, fallbacks, and auditability.")

with st.sidebar:
    st.subheader("Intake Metadata")
    department = st.selectbox("Department", ["People Ops", "IT", "Finance", "Customer Ops", "Other"])
    urgency = st.selectbox("Urgency", ["low", "medium", "high"])
    employee_name = st.text_input("Employee name (optional)", value="")
    st.divider()
    st.subheader("Controls")
    threshold_note = "Confidence threshold is hard-coded at 0.70 (see src/workflow.py)."
    st.info(threshold_note)

default_text = "I tried to redeem my award but the order shows pending and I never got a confirmation email."
message = st.text_area("Request message", value=default_text, height=140)

colA, colB, colC = st.columns([1, 1, 2])
with colA:
    run = st.button("Run triage", type="primary")
with colB:
    clear = st.button("Clear")
with colC:
    st.write("")

if clear:
    st.rerun()

if run:
    request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
    intake = IntakeRequest(
        request_id=request_id,
        employee_name=employee_name.strip() or None,
        department=department,
        urgency=urgency,
        message=message.strip(),
    )

    audit = build_audit_log()
    audit.append(audit_event("intake_received", {"request_id": request_id, "department": department, "urgency": urgency}))

    cls = classify(intake.message)
    audit.append(audit_event("ai_classification", {"category": cls.category, "confidence": cls.confidence, "rationale": cls.rationale}))

    decision = route(cls, urgency=urgency)
    audit.append(audit_event("workflow_routed", {"destination": decision.destination, "requires_human_review": decision.requires_human_review, "reasons": decision.reasons}))

    ticket = TicketRecord(
        request=intake,
        classification=cls,
        routing=decision,
        created_at_iso=now_iso(),
        audit_log=audit,
    )

    st.success(f"Created ticket {request_id} → **{decision.destination}**")

    left, right = st.columns(2)
    with left:
        st.subheader("Classification")
        st.metric("Category", cls.category)
        st.metric("Confidence", f"{cls.confidence:.2f}")
        st.write("**Rationale**")
        st.write(cls.rationale)
        if cls.extracted_entities:
            st.write("**Extracted signals**")
            st.json(cls.extracted_entities)

    with right:
        st.subheader("Routing decision")
        st.write(f"**Destination:** {decision.destination}")
        st.write(f"**Action:** {decision.action}")
        st.write(f"**Human review required:** {'Yes' if decision.requires_human_review else 'No'}")
        if decision.reasons:
            st.write("**Reasons**")
            for r in decision.reasons:
                st.write(f"- {r}")

    st.subheader("Structured ticket (JSON)")
    st.json(json.loads(ticket.model_dump_json()))

    st.subheader("Audit log")
    st.table([{"ts": e["ts"], "event": e["event"], "details": json.dumps(e["details"])} for e in ticket.audit_log])
