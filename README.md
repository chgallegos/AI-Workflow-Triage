# AI Workflow Triage Bot (Automation Engineer Demo)

A lightweight demo that mirrors an enterprise automation pattern: **intake → AI classification → workflow routing → structured ticket + audit log → safe fallback to human review**.

This project is intentionally designed to demonstrate:
- Business-process-first automation thinking
- Workflow-based routing (Power Automate style)
- Responsible AI usage (confidence thresholds + escalation)
- Clear, supportable outputs (JSON tickets + auditability)

## What it does
Given an unstructured request message, the app:
1. Classifies intent (category + confidence + rationale)
2. Routes the request to a destination queue
3. Generates a structured JSON ticket record
4. Writes an audit log of all decisions
5. Escalates low-confidence cases to **Human Review**

## Categories supported
- recognition_help
- award_fulfillment_issue
- nomination_guidance
- policy_eligibility
- access_permissions
- unknown (fallback)

## Responsible AI guardrails (demo)
- Confidence threshold (0.70) controls auto-routing
- Below threshold → **Human Review**
- Explainability: classification includes rationale
- No PII storage required (employee name is optional and unused in logic)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
