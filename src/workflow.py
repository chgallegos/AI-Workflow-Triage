from __future__ import annotations
from .schemas import ClassificationResult, RoutingDecision

CONFIDENCE_THRESHOLD = 0.70

CATEGORY_TO_QUEUE = {
    "recognition_help": "Recognition Ops",
    "award_fulfillment_issue": "Recognition Ops",
    "nomination_guidance": "HR Ops",
    "policy_eligibility": "HR Ops",
    "access_permissions": "IT Support",
    "unknown": "Human Review",
}

def route(classification: ClassificationResult, urgency: str) -> RoutingDecision:
    reasons = []
    requires_human = False

    if classification.confidence < CONFIDENCE_THRESHOLD:
        requires_human = True
        reasons.append(f"Confidence {classification.confidence:.2f} below threshold {CONFIDENCE_THRESHOLD:.2f}.")

    destination = CATEGORY_TO_QUEUE.get(classification.category, "Human Review")

    # If low confidence, force Human Review
    if requires_human:
        destination = "Human Review"

    # Adjust action by urgency
    if urgency == "high":
        reasons.append("High urgency: prioritize SLA and notify on-call.")
        action = "Create ticket + notify primary + on-call"
    else:
        action = "Create ticket + notify primary"

    # If auth issue suspected, steer toward IT even if borderline
    if classification.extracted_entities.get("possible_auth_issue") and not requires_human:
        destination = "IT Support"
        reasons.append("Auth-related signal detected; routing to IT Support.")

    return RoutingDecision(
        destination=destination,
        action=action,
        requires_human_review=requires_human,
        reasons=reasons,
    )
