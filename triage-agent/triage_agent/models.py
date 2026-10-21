from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    customer_name: str
    email: str
    subject: str
    body: str
    created_at: str = ""

    @property
    def text(self) -> str:
        return f"{self.subject}\n{self.body}"


@dataclass
class TriageResult:
    ticket: Ticket
    language: str
    category: str
    urgency: str
    reply: str
    needs_review: bool = False
    review_reasons: List[str] = field(default_factory=list)
    urgency_reasons: List[str] = field(default_factory=list)
    category_scores: Dict[str, int] = field(default_factory=dict)
