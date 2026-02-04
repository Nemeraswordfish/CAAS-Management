from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class Sensitivity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class DecisionStrategy(str, Enum):
    GRANT = "grant_raw"
    MASK = "mask"
    DENY = "deny"


@dataclass
class RequestContext:
    data_principal_id: str
    requester_email: str
    purpose: str
    domain: str
    attributes: List[str]
    receiving_entity: str
    source_ip: str
    request_timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConsentArtifact:
    artifact_id: str
    data_principal_id: str
    purpose_id: str
    granted_at: datetime
    expires_at: datetime
    active: bool
    languages: List[str]
    cookie_preferences: Dict[str, bool]


@dataclass
class Decision:
    strategy: DecisionStrategy
    trust_score: float
    sensitivity: Sensitivity
    anonymization_score: float
    legal_basis: str
    rationale: str


@dataclass
class AuditEntry:
    action: str
    metadata: Dict[str, str]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    hash: Optional[str] = None
    previous_hash: Optional[str] = None
