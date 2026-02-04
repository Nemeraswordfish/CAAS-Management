from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4


@dataclass
class GrievanceTicket:
    reference_id: str
    data_principal_id: str
    description: str
    created_at: datetime
    status: str
    due_at: datetime
    escalated: bool = False


class GrievanceManager:
    def __init__(self, sla_days: int = 30) -> None:
        self._tickets: Dict[str, GrievanceTicket] = {}
        self._sla_days = sla_days

    def file_grievance(self, data_principal_id: str, description: str) -> GrievanceTicket:
        reference_id = str(uuid4())
        created_at = datetime.utcnow()
        ticket = GrievanceTicket(
            reference_id=reference_id,
            data_principal_id=data_principal_id,
            description=description,
            created_at=created_at,
            status="open",
            due_at=created_at + timedelta(days=self._sla_days),
        )
        self._tickets[reference_id] = ticket
        return ticket

    def update_status(self, reference_id: str, status: str) -> GrievanceTicket:
        ticket = self._tickets[reference_id]
        ticket.status = status
        return ticket

    def check_escalations(self) -> Dict[str, GrievanceTicket]:
        escalations = {}
        now = datetime.utcnow()
        for reference_id, ticket in self._tickets.items():
            if ticket.status != "resolved" and ticket.due_at < now:
                ticket.escalated = True
                escalations[reference_id] = ticket
        return escalations
