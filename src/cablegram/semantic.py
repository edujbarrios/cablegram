"""Small, inspectable semantic representation experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class Fact:
    """An explicit fact supplied by a caller; Cablegram does not infer it."""

    subject: str
    predicate: str
    object: str
    qualifiers: tuple[str, ...] = field(default_factory=tuple)
    confidence: str = "stated"

    def render(self) -> str:
        base = f"{self.subject} | {self.predicate} | {self.object}"
        extras = list(self.qualifiers)
        if self.confidence != "stated":
            extras.append(f"confidence={self.confidence}")
        return base if not extras else f"{base} | {'; '.join(extras)}"


@dataclass(frozen=True, slots=True)
class SemanticMessage:
    """A deliberately narrow, caller-authored fact container."""

    facts: tuple[Fact, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SemanticMessage":
        raw_facts = data.get("facts", ())
        facts = tuple(
            Fact(
                subject=str(item["subject"]),
                predicate=str(item["predicate"]),
                object=str(item["object"]),
                qualifiers=tuple(str(value) for value in item.get("qualifiers", ())),
                confidence=str(item.get("confidence", "stated")),
            )
            for item in raw_facts
        )
        return cls(facts=facts)

    def to_dict(self) -> dict[str, Any]:
        return {"facts": [asdict(fact) for fact in self.facts]}

    def render(self) -> str:
        return "\n".join(fact.render() for fact in self.facts)

    @classmethod
    def from_facts(cls, facts: Iterable[Fact]) -> "SemanticMessage":
        return cls(facts=tuple(facts))
