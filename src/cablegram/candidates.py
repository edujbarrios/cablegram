"""Candidate generation and conservative selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cablegram.measure import Measurement, measure
from cablegram.optimize import available_rules, optimize
from cablegram.tokenizer import Tokenizer
from cablegram.verify import VerificationResult, verify


@dataclass(frozen=True, slots=True)
class Candidate:
    name: str
    text: str
    measurement: Measurement
    verification: VerificationResult

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "text": self.text,
            "measurement": self.measurement.as_dict(),
            "verification": self.verification.as_dict(),
        }


def generate_candidates(text: str, tokenizer: Tokenizer | None = None) -> tuple[Candidate, ...]:
    """Generate auditable deterministic candidates, including the original."""

    candidates: list[tuple[str, str]] = [("original", text)]
    for rule in available_rules():
        result = optimize(text, tokenizer=tokenizer, rules=(rule,))
        candidates.append((rule, result.optimized))
    all_rules = optimize(text, tokenizer=tokenizer)
    candidates.append(("all-rules", all_rules.optimized))

    unique: dict[str, str] = {}
    for name, candidate_text in candidates:
        unique.setdefault(candidate_text, name)

    return tuple(
        Candidate(
            name=name,
            text=candidate_text,
            measurement=measure(candidate_text, tokenizer=tokenizer),
            verification=verify(text, candidate_text),
        )
        for candidate_text, name in unique.items()
    )


def select_candidate(text: str, tokenizer: Tokenizer | None = None) -> Candidate:
    """Select the smallest candidate that passes deterministic invariants."""

    candidates = generate_candidates(text, tokenizer=tokenizer)
    passing = [candidate for candidate in candidates if candidate.verification.passed]
    return min(passing, key=lambda candidate: (candidate.measurement.tokens, len(candidate.text)))
