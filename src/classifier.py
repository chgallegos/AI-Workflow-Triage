from __future__ import annotations
import re
from typing import Tuple, Dict, Any
from .schemas import ClassificationResult, RequestCategory

# Lightweight “AI-like” classifier:
# - keyword scoring
# - confidence based on margin + match count
# - rationale for explainability

CATEGORY_KEYWORDS = {
    "recognition_help": [
        "how do i recognize", "send recognition", "ecard", "recognize", "shoutout",
        "post recognition", "points", "give points", "award someone"
    ],
    "award_fulfillment_issue": [
        "didn't receive", "not received", "shipping", "delivery", "redeem", "redemption",
        "order", "status", "tracking", "gift", "catalog", "award store"
    ],
    "nomination_guidance": [
        "nominate", "nomination", "recommend", "submission", "criteria", "who can be nominated"
    ],
    "policy_eligibility": [
        "policy", "eligible", "eligibility", "limit", "rules", "can i", "allowed", "restriction"
    ],
    "access_permissions": [
        "can't access", "permission", "login", "sso", "error", "access denied", "role", "group"
    ],
}

def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def _score(text: str) -> Tuple[RequestCategory, Dict[str, int]]:
    scores: Dict[str, int] = {k: 0 for k in CATEGORY_KEYWORDS.keys()}
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                scores[cat] += 2
    # Add token-level matches for flexibility
    tokens = set(re.findall(r"[a-zA-Z']+", text))
    token_map = {
        "award_fulfillment_issue": {"redeem", "redeemed", "tracking", "shipment", "deliver", "delivery", "order"},
        "recognition_help": {"recognition", "recognize", "ecard", "points", "award"},
        "access_permissions": {"login", "sso", "permission", "permissions", "access", "role", "group", "error"},
        "policy_eligibility": {"policy", "eligible", "eligibility", "limit", "rules"},
        "nomination_guidance": {"nominate", "nomination", "criteria"},
    }
    for cat, token_set in token_map.items():
        scores[cat] += len(tokens.intersection(token_set))
    best_cat = max(scores, key=lambda k: scores[k])
    return best_cat, scores

def classify(message: str) -> ClassificationResult:
    text = _normalize(message)
    best_cat, scores = _score(text)

    best_score = scores[best_cat]
    sorted_scores = sorted(scores.values(), reverse=True)
    second_best = sorted_scores[1] if len(sorted_scores) > 1 else 0
    margin = max(0, best_score - second_best)

    # Heuristic confidence:
    # - base on match count + margin, capped
    confidence = 0.2
    confidence += min(0.5, best_score * 0.08)
    confidence += min(0.3, margin * 0.12)
    confidence = min(1.0, max(0.0, confidence))

    if best_score <= 1:
        return ClassificationResult(
            category="unknown",
            confidence=0.35,
            rationale="Insufficient signal to classify confidently; routed to Human Review.",
            extracted_entities={},
        )

    rationale = f"Keyword+token scoring favored '{best_cat}' (score={best_score}, margin={margin})."
    extracted: Dict[str, Any] = {}

    # Simple entity extraction examples
    if "order" in text or "tracking" in text:
        extracted["possible_order_issue"] = True
    if "sso" in text or "login" in text:
        extracted["possible_auth_issue"] = True

    return ClassificationResult(
        category=best_cat, confidence=round(confidence, 2), rationale=rationale, extracted_entities=extracted
    )
