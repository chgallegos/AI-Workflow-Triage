# AI Workflow Intake & Routing (Automation Engineer Demo)

## 🚀 Live Demo (click to try)
👉 **https://ai-workflow-intake-routing.onrender.com/**

> Tip: Paste one of the test queries below and click **Run workflow**.

---

## Overview

A lightweight demo that mirrors a common **enterprise internal automation pattern**:

**intake → AI-assisted classification → workflow routing → structured output → safe human fallback**

This project is intentionally scoped to demonstrate how AI can be applied **responsibly** to support internal business operations, not as a customer-facing product.

---

## What this demonstrates (at a glance)

- **Business-process-first automation**
- **Workflow-based routing** (Power Automate–style thinking)
- **AI used only where it adds value** (unstructured text understanding)
- **Deterministic guardrails** (confidence thresholds, escalation)
- **Explainable, auditable outputs** (JSON + audit log)

---

## Try these test queries

Paste one of the following into the app to see different paths:

### 1) Award fulfillment issue → Recognition Ops

I redeemed my award but the order is still pending and I never received a confirmation or tracking email.


### 2) Access / login issue → IT Support

I can’t log in. SSO keeps failing and I get access denied when I try to sign in.


### 3) Policy question → HR Ops

Is there a monthly limit on how many points I’m allowed to give? Where is that policy documented?

### 4) Ambiguous request → Human Review (fallback)

Something seems off with recognition on my account and I’m not sure what changed.


---

## How AI is used (intentionally limited)

- AI is applied **only at intake** to interpret unstructured text
- It produces:
  - an intent category
  - a confidence score
  - an explainable rationale
- **AI does not make final workflow decisions**

Routing, escalation, and actions remain **deterministic and auditable**.

---

## Responsible AI guardrails

- Confidence threshold (0.70) controls auto-routing
- Below threshold → **Human Review**
- All AI-assisted decisions are logged
- No irreversible or policy-enforcing decisions are made by AI

---

## Implementation note

For demo simplicity, the AI layer uses deterministic classification logic to simulate AI behavior.  
In a production environment, this layer could be swapped for **Azure AI or Copilot** without changing the workflow, guardrails, or auditability.

---

## Intended use

This demo represents an **internal automation pattern** for operations teams (People Ops, IT, Finance, Recognition Admin), not a client-facing feature.

---

## Run locally (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
