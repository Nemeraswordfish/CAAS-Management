from __future__ import annotations

from dataclasses import dataclass


PERSONAL_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "proton.me",
    "protonmail.com",
}


@dataclass
class KYUResult:
    trust_score: float
    explanation: str


class KYUAgent:
    """Know-Your-User agent to compute requester trust score."""

    def calculate_trust_score(self, email: str, purpose: str) -> KYUResult:
        domain = email.split("@")[-1].lower()
        score = 0.5
        notes = []

        if domain not in PERSONAL_EMAIL_DOMAINS:
            score += 0.25
            notes.append("organizational email domain")
        else:
            score -= 0.1
            notes.append("personal email domain")

        if "self" in purpose.lower() or "personal" in purpose.lower():
            score -= 0.1
            notes.append("self-use purpose")
        else:
            score += 0.15
            notes.append("organizational purpose")

        score = min(max(score, 0.0), 1.0)
        explanation = ", ".join(notes)
        return KYUResult(trust_score=score, explanation=explanation)
