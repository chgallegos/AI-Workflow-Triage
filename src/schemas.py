from __future__ import annotations
from typing import Literal, Optional, Dict, Any, List
from pydantic import BaseModel, Field

RequestCategory = Literal[
    "recognition_help",
    "award_fulfillment_issue",
    "nomination_guidance",
    "policy_eligibility",
    "access_permissions",
    "unknown",
]

QueueDestination = Literal[
    "Recognition Ops",
    "HR Ops",
    "IT Support",
    "Finance Ops",
    "Human Review",
]

Urgency = Literal["low", "medium", "high"]

class IntakeRequest(BaseModel):
    request_id: str
    employee_name: Optional[str] = None
    department: str
    urgency: Urgency
    message: str

class ClassificationResult(BaseModel):
    category: RequestCategory
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)

class RoutingDecision(BaseModel):
    destination: QueueDestination
    action: str
    requires_human_review: bool
    reasons: List[str] = Field(default_factory=list)

class TicketRecord(BaseModel):
    request: IntakeRequest
    classification: ClassificationResult
    routing: RoutingDecision
    created_at_iso: str
    audit_log: List[Dict[str, Any]]
