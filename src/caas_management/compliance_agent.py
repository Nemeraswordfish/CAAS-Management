from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from caas_management.models import Sensitivity


@dataclass
class LegalRule:
    domain: str
    sensitive_attributes: List[str]
    default_sensitivity: Sensitivity


class LegalRulesRepository:
    def __init__(self) -> None:
        self._rules: Dict[str, LegalRule] = {
            "health": LegalRule(
                domain="health",
                sensitive_attributes=["diagnosis", "medical_history"],
                default_sensitivity=Sensitivity.HIGH,
            ),
            "finance": LegalRule(
                domain="finance",
                sensitive_attributes=["income", "credit_score", "loan"],
                default_sensitivity=Sensitivity.HIGH,
            ),
            "identity": LegalRule(
                domain="identity",
                sensitive_attributes=["aadhaar", "passport"],
                default_sensitivity=Sensitivity.MODERATE,
            ),
        }

    def lookup(self, domain: str) -> LegalRule:
        return self._rules.get(
            domain,
            LegalRule(
                domain=domain,
                sensitive_attributes=[],
                default_sensitivity=Sensitivity.LOW,
            ),
        )


@dataclass
class ComplianceResult:
    sensitivity: Sensitivity
    explanation: str


class ComplianceAgent:
    """Agent to classify data sensitivity based on domain and attributes."""

    def __init__(self, rules_repo: LegalRulesRepository | None = None) -> None:
        self.rules_repo = rules_repo or LegalRulesRepository()

    def classify(self, domain: str, attributes: List[str]) -> ComplianceResult:
        rules = self.rules_repo.lookup(domain)
        normalized_attributes = {attr.lower() for attr in attributes}
        matched = [
            attr
            for attr in rules.sensitive_attributes
            if attr.lower() in normalized_attributes
        ]
        if matched:
            sensitivity = rules.default_sensitivity
            explanation = f"Matched sensitive attributes: {', '.join(matched)}"
        else:
            sensitivity = rules.default_sensitivity
            explanation = "No sensitive attribute matches; using default sensitivity"
        return ComplianceResult(sensitivity=sensitivity, explanation=explanation)
