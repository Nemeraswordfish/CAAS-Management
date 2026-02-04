from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List
from uuid import uuid4

from caas_management.models import ConsentArtifact


SUPPORTED_LANGUAGES = [
    "en",
    "hi",
    "bn",
    "te",
    "mr",
    "ta",
    "ur",
    "gu",
    "kn",
    "ml",
    "or",
    "pa",
    "as",
    "mai",
    "sa",
    "ks",
    "sd",
    "ne",
    "kok",
    "doi",
    "mni",
    "sat",
]


@dataclass
class ConsentValidationResult:
    valid: bool
    reason: str


class ConsentLifecycle:
    def __init__(self) -> None:
        self._artifacts: Dict[str, ConsentArtifact] = {}

    def collect_consent(
        self,
        data_principal_id: str,
        purpose_id: str,
        languages: List[str],
        cookie_preferences: Dict[str, bool],
        valid_days: int = 365,
    ) -> ConsentArtifact:
        if len(languages) != len(set(languages)):
            raise ValueError("Duplicate languages are not allowed")
        if not set(languages).issubset(SUPPORTED_LANGUAGES):
            raise ValueError("Unsupported language supplied")
        artifact_id = str(uuid4())
        granted_at = datetime.utcnow()
        expires_at = granted_at + timedelta(days=valid_days)
        artifact = ConsentArtifact(
            artifact_id=artifact_id,
            data_principal_id=data_principal_id,
            purpose_id=purpose_id,
            granted_at=granted_at,
            expires_at=expires_at,
            active=True,
            languages=languages,
            cookie_preferences=cookie_preferences,
        )
        self._artifacts[artifact_id] = artifact
        return artifact

    def validate_consent(self, artifact_id: str) -> ConsentValidationResult:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return ConsentValidationResult(False, "Consent artifact not found")
        if not artifact.active:
            return ConsentValidationResult(False, "Consent artifact withdrawn")
        if artifact.expires_at < datetime.utcnow():
            return ConsentValidationResult(False, "Consent artifact expired")
        return ConsentValidationResult(True, "Consent artifact is valid")

    def renew_consent(self, artifact_id: str, extension_days: int = 365) -> ConsentArtifact:
        artifact = self._artifacts[artifact_id]
        artifact.expires_at = max(artifact.expires_at, datetime.utcnow()) + timedelta(
            days=extension_days
        )
        return artifact

    def withdraw_consent(self, artifact_id: str) -> ConsentArtifact:
        artifact = self._artifacts[artifact_id]
        artifact.active = False
        return artifact

    def update_cookie_preferences(
        self, artifact_id: str, preferences: Dict[str, bool]
    ) -> ConsentArtifact:
        artifact = self._artifacts[artifact_id]
        artifact.cookie_preferences = preferences
        return artifact
