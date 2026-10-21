"""Rule-based support-ticket triage agent (French / English)."""

from .models import Ticket, TriageResult
from .pipeline import read_tickets, triage_all, triage_ticket

__all__ = ["Ticket", "TriageResult", "triage_ticket", "triage_all", "read_tickets"]
