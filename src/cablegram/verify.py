"""Deterministic preservation checks for conservative optimization."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any


_NUMBER_RE = re.compile(r"(?<!\w)[+-]?\d+(?:[.,]\d+)?%?(?!\w)")
_URL_RE = re.compile(r"https?://[^\s)\]>]+")
_PATH_RE = re.compile(r"(?:[A-Za-z0-9_.-]+/)+(?:[A-Za-z0-9_.-]+)")
_BACKTICK_RE = re.compile(r"`[^`\n]+`")
_NEGATION_RE = re.compile(r"\b(?:no|not|never|without|none|cannot|can't|won't|don't|doesn't|isn't|aren't)\b", re.IGNORECASE)
_UNCERTAINTY_RE = re.compile(r"\b(?:possible|possibly|likely|unlikely|maybe|may|might|uncertain|unconfirmed|suspected|appears?)\b", re.IGNORECASE)
_CONSTRAINT_RE = re.compile(r"\b(?:must|mustn't|should|shouldn't|required|requirement|forbidden|prohibited|do not|don't)\b", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class Invariants:
    numbers: tuple[str, ...]
    negations: tuple[str, ...]
    uncertainty: tuple[str, ...]
    constraints: tuple[str, ...]
    identifiers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class VerificationResult:
    passed: bool
    source: Invariants
    candidate: Invariants
    missing: dict[str, tuple[str, ...]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "source": self.source.as_dict(),
            "candidate": self.candidate.as_dict(),
            "missing": {key: list(values) for key, values in self.missing.items()},
        }


def _unique(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.casefold() for value in values))


def extract_invariants(text: str) -> Invariants:
    """Extract exact surface invariants that conservative rewrites should retain."""

    identifiers = _URL_RE.findall(text) + _PATH_RE.findall(text) + _BACKTICK_RE.findall(text)
    return Invariants(
        numbers=_unique(_NUMBER_RE.findall(text)),
        negations=_unique(_NEGATION_RE.findall(text)),
        uncertainty=_unique(_UNCERTAINTY_RE.findall(text)),
        constraints=_unique(_CONSTRAINT_RE.findall(text)),
        identifiers=_unique(identifiers),
    )


def verify(source: str, candidate: str) -> VerificationResult:
    """Require all extracted source invariants to remain explicitly present."""

    source_invariants = extract_invariants(source)
    candidate_invariants = extract_invariants(candidate)
    missing: dict[str, tuple[str, ...]] = {}
    for field in ("numbers", "negations", "uncertainty", "constraints", "identifiers"):
        source_values = set(getattr(source_invariants, field))
        candidate_values = set(getattr(candidate_invariants, field))
        absent = tuple(sorted(source_values - candidate_values))
        if absent:
            missing[field] = absent
    return VerificationResult(
        passed=not missing,
        source=source_invariants,
        candidate=candidate_invariants,
        missing=missing,
    )
