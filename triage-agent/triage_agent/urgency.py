"""Urgency rules: P1 (critical) > P2 (blocking for one user / wrong amount) > P3 (question)."""

import re
from dataclasses import dataclass
from typing import List, Tuple

from .text import compile_pattern, first_match, normalize

PAYMENT_WINDOW = 6

PAYMENT_TERM = re.compile(r"paiements?|payments?")
PAYMENT_BLOCKED = compile_pattern(
    r"bloque\w*|blocked|refuse\w*|declined|rejet\w*|rejected|echou\w*|echec|failed|failing|"
    r"fails|impossible|can t|cannot|won t go through|ne passe pas|suspendu|suspended"
)
DOUBLE_CHARGE = [
    compile_pattern(p)
    for p in (
        r"(prelev|debit|factur|pay|charg|bill)\w* (deux fois|twice|2 fois)",
        r"(paiement|prelevement|debit|payment|charge)s? (\w+ ){0,3}en double",
        r"double (prelevement|debit|paiement|facturation|charge|payment)s?",
        r"duplicate (charge|payment)s?",
    )
]
P1_PATTERNS = [
    compile_pattern(p)
    for p in (
        r"panne", r"outage", r"(site|app|application|plateforme|platform|service) (is )?down",
        r"toute l equipe|toute notre equipe|tous (les|nos) (utilisateurs|collaborateurs)",
        r"whole team|entire team|all (of )?(our )?users",
        r"nobody can|no one can|personne ne peut",
        r"perte de donnees|donnees perdues|data loss|lost (all )?(our )?data",
        r"pirat\w*|hack\w*|fraud\w*|fraude|suspicious|breach|faille de securite",
    )
]
P2_PATTERNS = [
    compile_pattern(p)
    for p in (
        r"bloque\w*|blocked|locked out|verrouill\w*",
        r"impossible|can t|cannot|unable|n arrive plus|n arrive pas",
        r"ne fonctionne plus|ne marche plus|not working",
        r"erreurs?|errors?|crash\w*|plante\w*",
        r"incorrect\w*|wrong|errone\w*|faux|fausse",
        r"rembours\w*|refunds?",
    )
]
ESCALATION_PATTERNS = [
    compile_pattern(p)
    for p in (
        r"urgent\w*|urgence", r"asap|as soon as possible|au plus vite|des que possible",
        r"immediately|immediatement", r"critical|critique",
    )
]


@dataclass(frozen=True)
class Urgency:
    level: str  # "P1" | "P2" | "P3"
    reasons: Tuple[str, ...]


def payment_problem(text: str) -> str:
    """Return a reason if a payment is blocked/refused/failed or was charged twice, else ''."""
    norm = normalize(text)
    hit = first_match(norm, DOUBLE_CHARGE)
    if hit:
        return f"payment charged twice ('{hit}')"
    words = norm.split()
    for i, word in enumerate(words):
        if PAYMENT_TERM.fullmatch(word):
            window = " ".join(words[max(0, i - PAYMENT_WINDOW): i + PAYMENT_WINDOW + 1])
            m = PAYMENT_BLOCKED.search(window)
            if m:
                return f"payment blocked ('{word}' ... '{m.group(0)}')"
    return ""


def assess_urgency(text: str) -> Urgency:
    norm = normalize(text)
    reasons: List[str] = []
    level = 3

    payment = payment_problem(text)
    if payment:
        return Urgency("P1", (f"always P1: {payment}",))

    hit = first_match(norm, P1_PATTERNS)
    if hit:
        level = 1
        reasons.append(f"critical impact ('{hit}')")
    else:
        hit = first_match(norm, P2_PATTERNS)
        if hit:
            level = 2
            reasons.append(f"user blocked or wrong result ('{hit}')")

    hit = first_match(norm, ESCALATION_PATTERNS)
    if hit and level > 1:
        level -= 1
        reasons.append(f"escalated one level ('{hit}')")

    if not reasons:
        reasons.append("no impact keywords: question or request")
    return Urgency(f"P{level}", tuple(reasons))
