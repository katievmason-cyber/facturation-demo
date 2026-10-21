import re
from dataclasses import dataclass

from .text import tokens

FRENCH_WORDS = frozenset(
    """le la les un une des du de et est sont pas ne nous vous je il elle pour avec dans
    que qui mais notre votre nos vos ce cette ces mon ma mes au aux bonjour merci depuis
    tres fait ete avons pouvez sur leur ou alors quand comme aussi cordialement""".split()
)
ENGLISH_WORDS = frozenset(
    """the and is are not we you i it for with that which but our your this these my
    to of from hello hi thanks thank since very have has been can please when after
    there they would could should what how""".split()
)
FRENCH_CHARS = re.compile(r"[àâçéèêëîïôûùüÿœæ]")
ACCENT_WEIGHT = 0.5
MIN_EVIDENCE = 3
MIN_CONFIDENCE = 0.65


@dataclass(frozen=True)
class LanguageResult:
    language: str  # "fr" or "en"
    confidence: float
    ambiguous: bool


def detect_language(text: str) -> LanguageResult:
    words = tokens(text)
    fr = sum(1 for w in words if w in FRENCH_WORDS)
    fr += ACCENT_WEIGHT * len(FRENCH_CHARS.findall(text.lower()))
    en = sum(1 for w in words if w in ENGLISH_WORDS)
    total = fr + en
    if total == 0:
        return LanguageResult("en", 0.0, True)
    language = "fr" if fr > en else "en"
    confidence = max(fr, en) / total
    ambiguous = total < MIN_EVIDENCE or confidence < MIN_CONFIDENCE
    return LanguageResult(language, round(confidence, 2), ambiguous)
