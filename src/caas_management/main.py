from __future__ import annotations

from caas_management.audit import AuditTrail
from caas_management.compliance_agent import ComplianceAgent
from caas_management.consent import ConsentLifecycle
from caas_management.grievance import GrievanceManager
from caas_management.interoperability import InteroperabilityGateway
from caas_management.kyu_agent import KYUAgent
from caas_management.models import AuditEntry, RequestContext
from caas_management.orchestrator import ComplianceOrchestrator, OrchestrationInputs
from caas_management.perception import CompliancePipeline


def run_demo() -> None:
    request = RequestContext(
        data_principal_id="dp-001",
        requester_email="analyst@bank.example",
        purpose="Loan underwriting",
        domain="finance",
        attributes=["income", "employment"],
        receiving_entity="Acme Bank",
        source_ip="203.0.113.42",
    )

    pipeline = CompliancePipeline()
    rule_tuple = pipeline.to_tuple(
        request,
        legal_text="DPDP consent required for finance data; allow withdrawal and renewal.",
    )

    kyu_agent = KYUAgent()
    kyu_result = kyu_agent.calculate_trust_score(
        request.requester_email, request.purpose
    )

    compliance_agent = ComplianceAgent()
    compliance_result = compliance_agent.classify(request.domain, request.attributes)

    orchestrator = ComplianceOrchestrator()
    decision = orchestrator.decide(
        OrchestrationInputs(
            trust_score=kyu_result.trust_score, sensitivity=compliance_result.sensitivity
        )
    )

    consent_lifecycle = ConsentLifecycle()
    consent = consent_lifecycle.collect_consent(
        data_principal_id=request.data_principal_id,
        purpose_id="loan-underwriting",
        languages=["en", "hi"],
        cookie_preferences={"essential": True, "marketing": False},
    )

    audit_trail = AuditTrail()
    audit_trail.append(
        AuditEntry(
            action="consent_granted",
            metadata={
                "user_id": request.data_principal_id,
                "purpose_id": consent.purpose_id,
                "source_ip": request.source_ip,
            },
        )
    )

    gateway = InteroperabilityGateway()
    gateway.register("Acme Bank", "https://api.acmebank.example/consent")
    push_result = gateway.push_consent_status(
        "Acme Bank", {"artifact_id": consent.artifact_id, "status": "active"}
    )

    grievance_manager = GrievanceManager()
    grievance = grievance_manager.file_grievance(
        request.data_principal_id, "Need clarity on consent scope."
    )

    print("Rule tuple:", rule_tuple)
    print("KYU:", kyu_result)
    print("Compliance:", compliance_result)
    print("Decision:", decision)
    print("Consent:", consent)
    print("Audit hash:", audit_trail.entries[-1].hash)
    print("Interoperability:", push_result)
    print("Grievance:", grievance.reference_id)


if __name__ == "__main__":
    run_demo()
