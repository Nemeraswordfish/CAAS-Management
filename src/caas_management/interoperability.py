from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class FiduciaryEndpoint:
    name: str
    base_url: str


class InteroperabilityGateway:
    """Simulates push/pull consent status for Data Fiduciaries."""

    def __init__(self) -> None:
        self._registry: Dict[str, FiduciaryEndpoint] = {}

    def register(self, name: str, base_url: str) -> None:
        self._registry[name] = FiduciaryEndpoint(name=name, base_url=base_url)

    def push_consent_status(self, name: str, payload: Dict[str, str]) -> str:
        endpoint = self._registry[name]
        return f"Pushed consent update to {endpoint.base_url} with {payload}"

    def pull_consent_status(self, name: str, consent_id: str) -> str:
        endpoint = self._registry[name]
        return f"Pulled consent {consent_id} from {endpoint.base_url}"
