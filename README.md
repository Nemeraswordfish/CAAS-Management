# CAAS-Management
Composting as a Service Management Dashboard

## Agentic Compliance-as-a-Service (CaaS) Consent Manager Requirements
The following requirements outline how the platform should evolve into an **agentic** compliance system for India’s DPDP Act, with autonomous agents, transparent decisioning, and interoperable consent operations.

### 1) Agentic Architecture & Core Components
**Layered architecture** with autonomous agents and explicit orchestration:

- **Perception Layer (Input Processing)**
  - Ingest heterogeneous inputs (user requests, legal texts, fiduciary metadata).
  - Run a **Compliance Pipeline** (NLP + rule extraction) that converts DPDP Act clauses into structured tuples such as:
    - `<Data Principal, Domain, Rules, Receiving Entity>`.

- **Reasoning Layer (Specialized Agents)**
  - **Know-Your-User (KYU) Agent**
    - Compute a **Trust Score** for requesters using signals like:
      - Email domain (organizational vs. personal).
      - Declared purpose (self-use vs. organizational use).
  - **Compliance Agent**
    - Determine **Data Sensitivity** by querying a legal rules repository.
    - Classify requested data into **Low / Moderate / High** sensitivity based on domain and attributes (e.g., Health, Finance, Income).

- **Orchestration Layer (Decision Engine)**
  - A **Compliance Orchestrator** synthesizes:
    - KYU Trust Score
    - Compliance Agent Data Sensitivity
  - It selects strategies such as **grant raw access**, **mask/anonymize**, or **deny**.

### 2) Functional Requirements for Consent Management
Consent must be managed end-to-end per MeitY’s BRD and DPDP Rules:

| Lifecycle Stage | Agentic Requirement |
| --- | --- |
| **Collection** | Show **purpose-specific** notices in English + all 8th Schedule languages. Prevent bundled consent. |
| **Validation** | Validate via API that consent artifact exists, is active, and not withdrawn before processing. |
| **Renewal** | Track expirations and proactively notify Data Principals to renew per purpose. |
| **Withdrawal** | Provide dashboard-based revocation; trigger **real-time APIs** to stop processing across fiduciaries. |
| **Cookie Management** | Granular consent for essential vs. marketing cookies; log preferences. |

### 3) Regulatory & Technical Prerequisites
Operational constraints for DPB recognition:

- **Legal Entity & Net Worth**: Indian-registered company with **₹2 crore** minimum net worth.
- **Interoperability**: Standard APIs for real-time push/pull with multiple Data Fiduciaries (banks, telcos, apps).
- **Security & Immutable Logging**: Tamper-proof audit trail for every consent action, with metadata (User ID, Timestamp, Purpose ID, Source IP) and cryptographic hashing (e.g., blockchain).
- **Vulnerable Data Handling**: Verification for children/persons with disabilities (e.g., DigiLocker for parental consent).

### 4) Explainability and Transparency
Agentic decisions must be interpretable and user-facing:

- **Legal Justification**: Human-readable explanation anchored to DPDP Act basis (e.g., “Shared under legal obligation”).
- **Anonymization Scoring**: Display a **0–1 score** to quantify data masking/anonymization.

### 5) Operational Infrastructure
Supporting governance and oversight workflows:

- **Grievance Redressal**: Complaint logging, auto-reference numbers, status tracking, and auto-escalation to DPO on SLA breach.
- **Data Residence**: Consent metadata and audit logs should reside in India to support DPB audits.

### Workflow Summary
1. **Perception**: Identify the request (e.g., “Read Income Data”).
2. **Reasoning**: KYU Agent evaluates requester; Compliance Agent marks “Income” as high sensitivity.
3. **Orchestration**: Determine that explicit, granular consent is required.
4. **Action**: Present a purpose-specific consent prompt, generate a cryptographically secured **Consent Artifact**, and log the event.

## Prototype Modules
This repo now includes a lightweight Python prototype implementing the required agentic modules:

- **Perception**: `CompliancePipeline` (rule extraction and tuple creation).
- **Reasoning**: `KYUAgent` + `ComplianceAgent` (trust and sensitivity).
- **Orchestration**: `ComplianceOrchestrator` (grant/mask/deny decisions).
- **Consent Lifecycle**: `ConsentLifecycle` (collect/validate/renew/withdraw).
- **Audit Trail**: `AuditTrail` (hash-chained audit entries).
- **Interoperability**: `InteroperabilityGateway` (push/pull consent status).
- **Grievance Redressal**: `GrievanceManager` (ticketing + escalation checks).

### Run the Demo
```bash
PYTHONPATH=src python -m caas_management.main
```
