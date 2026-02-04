from __future__ import annotations

from dataclasses import dataclass

from caas_management.models import Decision, DecisionStrategy, Sensitivity


@dataclass
class OrchestrationInputs:
    trust_score: float
    sensitivity: Sensitivity


class ComplianceOrchestrator:
    """Decision engine to pick grant/mask/deny strategies."""

    def decide(self, inputs: OrchestrationInputs) -> Decision:
        if inputs.sensitivity == Sensitivity.HIGH:
            if inputs.trust_score >= 0.7:
                strategy = DecisionStrategy.MASK
                anonymization_score = 0.6
                legal_basis = "Explicit consent required for high-sensitivity data"
                rationale = "High sensitivity data masked; trust score supports access"
            else:
                strategy = DecisionStrategy.DENY
                anonymization_score = 1.0
                legal_basis = "Consent or trust threshold unmet"
                rationale = "High sensitivity data denied due to low trust score"
        elif inputs.sensitivity == Sensitivity.MODERATE:
            if inputs.trust_score >= 0.4:
                strategy = DecisionStrategy.MASK
                anonymization_score = 0.4
                legal_basis = "Purpose-limited sharing with safeguards"
                rationale = "Moderate sensitivity data shared with masking"
            else:
                strategy = DecisionStrategy.DENY
                anonymization_score = 1.0
                legal_basis = "Insufficient trust for moderate sensitivity"
                rationale = "Moderate sensitivity data denied"
        else:
            if inputs.trust_score >= 0.3:
                strategy = DecisionStrategy.GRANT
                anonymization_score = 0.0
                legal_basis = "Low sensitivity data allowed with valid purpose"
                rationale = "Low sensitivity data granted"
            else:
                strategy = DecisionStrategy.MASK
                anonymization_score = 0.2
                legal_basis = "Low sensitivity data shared with minimal masking"
                rationale = "Low trust score triggers lightweight masking"

        return Decision(
            strategy=strategy,
            trust_score=inputs.trust_score,
            sensitivity=inputs.sensitivity,
            anonymization_score=anonymization_score,
            legal_basis=legal_basis,
            rationale=rationale,
        )
