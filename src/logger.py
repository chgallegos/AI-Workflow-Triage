from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime, timezone

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def audit_event(event: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ts": now_iso(),
        "event": event,
        "details": details,
    }

def build_audit_log() -> List[Dict[str, Any]]:
    return []
