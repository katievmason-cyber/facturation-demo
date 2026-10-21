import re
import unicodedata
from typing import Iterable, List, Pattern, Tuple


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def normalize(text: str) -> str:
    """Lowercase, drop accents, and keep only letters/digits separated by single spaces.

    Apostrophes become spaces, so "l'équipe" -> "l equipe" and "can't" -> "can t".
    All keyword patterns are written against this normalized form.
    """
    text = strip_accents(text.lower())
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return text.strip()


def tokens(text: str) -> List[str]:
    return normalize(text).split()


def compile_pattern(pattern: str) -> Pattern[str]:
    return re.compile(rf"\b(?:{pattern})\b")


def compile_weighted(items: Iterable[Tuple[str, int]]) -> List[Tuple[Pattern[str], int]]:
    return [(compile_pattern(p), w) for p, w in items]


def first_match(normalized_text: str, patterns: Iterable[Pattern[str]]):
    for rx in patterns:
        m = rx.search(normalized_text)
        if m:
            return m.group(0)
    return None
