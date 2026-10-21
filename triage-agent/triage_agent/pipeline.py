import csv
from typing import Iterable, List

from .classify import classify
from .language import detect_language
from .models import Ticket, TriageResult
from .reply import draft_reply
from .text import compile_pattern, normalize
from .urgency import assess_urgency

SENSITIVE_TOPICS = {
    "personal data request (GDPR)": compile_pattern(r"rgpd|gdpr"),
    "possible security incident": compile_pattern(
        r"pirat\w*|hack\w*|fraud\w*|fraude|suspicious|breach|faille de securite"
    ),
    "refund requested": compile_pattern(r"rembours\w*|refunds?|refunded"),
    "legal wording": compile_pattern(r"avocat|lawyer|legal|juridique|mise en demeure|litige"),
}

CSV_FIELDS = ["ticket_id", "customer_name", "email", "subject", "body", "created_at"]
OUTPUT_FIELDS = [
    "ticket_id", "language", "category", "urgency", "needs_review", "review_reasons",
    "urgency_reasons", "subject", "reply",
]


def read_tickets(path: str) -> List[Ticket]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = set(CSV_FIELDS[:5]) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
        return [Ticket(**{k: (row.get(k) or "").strip() for k in CSV_FIELDS}) for row in reader]


def triage_ticket(ticket: Ticket) -> TriageResult:
    text = ticket.text
    lang = detect_language(text)
    cls = classify(text)
    urgency = assess_urgency(text)

    review_reasons = []
    if lang.ambiguous:
        review_reasons.append(f"language unclear (confidence {lang.confidence})")
    if not cls.confident:
        review_reasons.append(cls.low_confidence_reason)
    norm = normalize(text)
    review_reasons += [topic for topic, rx in SENSITIVE_TOPICS.items() if rx.search(norm)]

    return TriageResult(
        ticket=ticket,
        language=lang.language,
        category=cls.category,
        urgency=urgency.level,
        reply=draft_reply(ticket, lang.language, cls.category, urgency.level),
        needs_review=bool(review_reasons),
        review_reasons=review_reasons,
        urgency_reasons=list(urgency.reasons),
        category_scores=cls.scores,
    )


def triage_all(tickets: Iterable[Ticket]) -> List[TriageResult]:
    return [triage_ticket(t) for t in tickets]


def write_results_csv(results: Iterable[TriageResult], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "ticket_id": r.ticket.ticket_id,
                "language": r.language,
                "category": r.category,
                "urgency": r.urgency,
                "needs_review": "yes" if r.needs_review else "no",
                "review_reasons": "; ".join(r.review_reasons),
                "urgency_reasons": "; ".join(r.urgency_reasons),
                "subject": r.ticket.subject,
                "reply": r.reply,
            })
