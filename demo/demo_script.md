# 90–120s Demo Script

## 1) What this is (10s)
“This is a lightweight AI workflow triage bot — it takes unstructured employee ops requests and routes them through a Power Automate-style workflow with confidence thresholds and safe fallbacks.”

## 2) Show a clear request (35s)
- Paste: “I redeemed my award but the order shows pending…”
- Click Run triage
- Point out:
  - Category + confidence
  - Routed to Recognition Ops
  - Structured JSON ticket

## 3) Show a risky/ambiguous request (35s)
- Paste something unclear: “I can’t see something I should be seeing…”
- Run triage
- Point out:
  - Lower confidence
  - Routed to Human Review
  - Audit log shows why

## 4) Close with alignment (15s)
“The goal is maintainable automation: explainable decisions, safe escalation, and structured outputs that are easy to support and extend.”
