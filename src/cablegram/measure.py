"""Deterministic text measurements."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any

from cablegram.tokenizer import Cl100kTokenizer, Tokenizer


@dataclass(frozen=True, slots=True)
class Measurement:
    """Counts for one text under a named tokenizer."""

    characters: int
    words: int
    tokens: int
    tokenizer: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def measure(text: str, tokenizer: Tokenizer | None = None) -> Measurement:
    """Measure Unicode code points, whitespace-delimited words, and tokens."""

    active_tokenizer = tokenizer or Cl100kTokenizer()
    return Measurement(
        characters=len(text),
        words=len(re.findall(r"\S+", text)),
        tokens=active_tokenizer.count(text),
        tokenizer=active_tokenizer.name,
    )
