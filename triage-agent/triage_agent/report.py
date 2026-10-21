from collections import Counter
from typing import List, Sequence

from .classify import CATEGORIES
from .models import TriageResult

URGENCIES = ("P1", "P2", "P3")
LANGUAGES = ("fr", "en")


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def _table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> List[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(_cell(str(c)) for c in row) + " |" for row in rows]
    return lines


def _count_rows(counter: Counter, keys: Sequence[str], total: int):
    return [(k, counter[k], f"{(100 * counter[k] / total) if total else 0:.0f} %") for k in keys]


def render_report(results: List[TriageResult], source: str = "") -> str:
    total = len(results)
    by_cat = Counter(r.category for r in results)
    by_urg = Counter(r.urgency for r in results)
    by_lang = Counter(r.language for r in results)
    review = [r for r in results if r.needs_review]

    out = ["# Rapport de triage / Triage report", ""]
    if source:
        out += [f"Source : `{source}`", ""]
    out += [
        f"- **Tickets :** {total}",
        f"- **P1 :** {by_urg['P1']}",
        f"- **À revoir par un humain / Needs human review :** {len(review)}",
        "",
        "## Par catégorie / By category", "",
        *_table(["Catégorie / Category", "Tickets", "%"], _count_rows(by_cat, CATEGORIES, total)), "",
        "## Par urgence / By urgency", "",
        *_table(["Urgence / Urgency", "Tickets", "%"], _count_rows(by_urg, URGENCIES, total)), "",
        "## Par langue / By language", "",
        *_table(["Langue / Language", "Tickets", "%"], _count_rows(by_lang, LANGUAGES, total)), "",
        "## Catégorie × urgence / Category × urgency", "",
    ]
    matrix = Counter((r.category, r.urgency) for r in results)
    out += _table(
        ["", *URGENCIES, "Total"],
        [(c, *(matrix[(c, u)] for u in URGENCIES), by_cat[c]) for c in CATEGORIES]
        + [("**Total**", *(by_urg[u] for u in URGENCIES), total)],
    )

    p1 = [r for r in results if r.urgency == "P1"]
    out += ["", "## Tickets P1", ""]
    out += _table(
        ["ID", "Catégorie", "Sujet / Subject", "Raison / Reason"],
        [(r.ticket.ticket_id, r.category, r.ticket.subject, "; ".join(r.urgency_reasons)) for r in p1],
    ) if p1 else ["_Aucun / None_"]

    out += ["", "## À revoir par un humain / Needs human review", ""]
    out += _table(
        ["ID", "Catégorie", "Urgence", "Raison / Reason"],
        [(r.ticket.ticket_id, r.category, r.urgency, "; ".join(r.review_reasons)) for r in review],
    ) if review else ["_Aucun / None_"]

    out += ["", "## Détail par ticket / Per-ticket detail", ""]
    out += _table(
        ["ID", "Langue", "Catégorie", "Urgence", "Revue", "Sujet / Subject", "Réponse proposée / Draft reply"],
        [
            (r.ticket.ticket_id, r.language, r.category, r.urgency, "oui" if r.needs_review else "non",
             r.ticket.subject, r.reply)
            for r in results
        ],
    )
    return "\n".join(out) + "\n"
