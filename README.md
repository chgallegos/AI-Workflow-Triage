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

## AI Usage & Model Strategy

This project is intentionally designed with a clear separation between **AI-assisted interpretation** and **deterministic workflow execution**.

### Where AI is used
AI is applied only at the **intake stage**, where it adds measurable value:
- Interpreting unstructured free-text requests
- Classifying intent into predefined categories
- Producing a confidence score
- Providing an explainable rationale for each decision

This mirrors common enterprise usage patterns where AI is best suited for **language understanding**, not for executing business-critical workflows.

### Current implementation (demo)
For the purposes of this demo, the AI layer is implemented using **deterministic classification logic** (keyword and token scoring). This approach was chosen to:
- Ensure full explainability
- Avoid external dependencies
- Keep the demo easy to run locally
- Highlight workflow design rather than model tuning

The output contract (category, confidence, rationale) is intentionally model-agnostic.

### Production-ready design
In a production environment, this classification layer could be replaced with:
- Microsoft Azure AI (Text Classification)
- Azure OpenAI (Copilot-style LLM orchestration)

without changing:
- Workflow logic
- Confidence thresholds
- Escalation rules
- Audit logging
- Downstream integrations

### Responsible AI guardrails
- Confidence thresholds control automation vs. human review
- Low-confidence cases are escalated automatically
- All AI-assisted decisions are logged with rationale
- AI does not make irreversible or policy-enforcing decisions

This design prioritizes **safety, maintainability, and supportability** while still benefiting from AI where it is most effective.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
