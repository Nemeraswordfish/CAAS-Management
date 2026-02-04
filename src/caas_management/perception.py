from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from caas_management.models import RequestContext


DOMAIN_KEYWORDS = {
    "health": {"health", "medical", "hospital", "diagnosis"},
    "finance": {"finance", "income", "salary", "loan", "credit"},
    "identity": {"id", "identity", "passport", "aadhaar"},
}


@dataclass
class RuleTuple:
    data_principal: str
    domain: str
    rules: List[str]
    receiving_entity: str


class CompliancePipeline:
    """Convert unstructured input into structured compliance tuples."""

    def extract_domain(self, text: str) -> str:
        lowered = text.lower()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                return domain
        return "general"

    def extract_rules(self, text: str) -> List[str]:
        lowered = text.lower()
        rules = []
        if "consent" in lowered:
            rules.append("consent_required")
        if "withdraw" in lowered or "revoke" in lowered:
            rules.append("withdrawal_supported")
        if "renew" in lowered or "expire" in lowered:
            rules.append("renewal_required")
        if not rules:
            rules.append("standard_processing")
        return rules

    def to_tuple(self, context: RequestContext, legal_text: str) -> RuleTuple:
        domain = self.extract_domain(legal_text or context.domain)
        rules = self.extract_rules(legal_text)
        return RuleTuple(
            data_principal=context.data_principal_id,
            domain=domain,
            rules=rules,
            receiving_entity=context.receiving_entity,
        )

    def normalize_request(self, payload: Dict[str, str]) -> RequestContext:
        return RequestContext(
            data_principal_id=payload["data_principal_id"],
            requester_email=payload["requester_email"],
            purpose=payload["purpose"],
            domain=payload["domain"],
            attributes=[item.strip() for item in payload["attributes"].split(",")],
            receiving_entity=payload["receiving_entity"],
            source_ip=payload.get("source_ip", "unknown"),
        )

    def summarize_inputs(self, inputs: Iterable[str]) -> str:
        return " | ".join(item.strip() for item in inputs if item)
