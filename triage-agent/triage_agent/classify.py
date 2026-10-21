from dataclasses import dataclass
from typing import Dict, Optional

from .text import compile_weighted, normalize

CATEGORIES = ("billing", "bug", "access", "other")
MIN_CONFIDENT_SCORE = 2

# Patterns are regexes matched against normalized (lowercase, accent-free) text.
KEYWORDS = {
    "billing": [
        (r"factur\w*", 1), (r"invoices?", 1), (r"tva", 2), (r"vat", 2), (r"montant", 1),
        (r"rembours\w*", 3), (r"refunds?|refunded", 3), (r"paiements?", 2), (r"payments?", 2),
        (r"prelev\w*", 2), (r"debite?s?", 2), (r"charged|charges?", 2),
        (r"abonnement", 2), (r"subscription", 2), (r"billing", 2),
        (r"carte bancaire|credit card|card declined", 2), (r"coordonnees bancaires", 2),
        (r"tarifs?|prix|price|pricing", 1), (r"discount|remise", 1), (r"checkout", 1),
    ],
    "bug": [
        (r"bugs?|bogue", 3), (r"erreurs?", 2), (r"errors?", 2), (r"crash\w*", 3), (r"plante\w*", 2),
        (r"ne fonctionne plus|ne marche plus|not working|doesn t work|stopped working", 3),
        (r"broken|casse", 2), (r"page blanche|blank page", 3), (r"500", 2),
        (r"freez\w*|fige\w*|bloque l ecran", 2), (r"timeout", 2), (r"slow|lent", 1),
        (r"exports?", 1), (r"mise a jour|update", 1),
    ],
    "access": [
        (r"connexion", 2), (r"connecter", 2), (r"log ?in|sign ?in", 2),
        (r"mot de passe|password", 3), (r"2fa|double authentification", 3), (r"sso", 3),
        (r"verrouill\w*|locked out", 3), (r"compte bloque|account locked", 3),
        (r"acces|access", 2), (r"identifiants?", 2), (r"invitation", 2), (r"invite\w*", 1),
        (r"droits|permissions?", 2), (r"reinitialis\w*|reset", 2),
    ],
    "other": [
        (r"suggestions?", 3), (r"fonctionnalite", 2), (r"feature request|feature", 2),
        (r"rgpd|gdpr", 3), (r"donnees personnelles|personal data", 2),
        (r"partenariat|partnership", 3), (r"demo", 2), (r"serait il possible|would be great", 2),
        (r"integration", 2), (r"question", 1),
    ],
}
_COMPILED = {cat: compile_weighted(items) for cat, items in KEYWORDS.items()}


@dataclass(frozen=True)
class Classification:
    category: str
    scores: Dict[str, int]
    low_confidence_reason: Optional[str] = None

    @property
    def confident(self) -> bool:
        return self.low_confidence_reason is None


def score(text: str) -> Dict[str, int]:
    norm = normalize(text)
    return {cat: sum(w for rx, w in pats if rx.search(norm)) for cat, pats in _COMPILED.items()}


def classify(text: str) -> Classification:
    scores = score(text)
    ranked = sorted(CATEGORIES, key=lambda c: (-scores[c], CATEGORIES.index(c)))
    top, second = ranked[0], ranked[1]
    if scores[top] == 0:
        return Classification("other", scores, "no category keywords matched")
    if scores[top] == scores[second]:
        return Classification(top, scores, f"tie between {top} and {second} ({scores[top]})")
    if scores[top] < MIN_CONFIDENT_SCORE:
        return Classification(top, scores, f"weak category signal (score {scores[top]})")
    return Classification(top, scores)
