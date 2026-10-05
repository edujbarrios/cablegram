"""Receiver-aware exact context compaction."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from cablegram.candidates import Candidate, select_candidate
from cablegram.tokenizer import Tokenizer


@dataclass(frozen=True, slots=True)
class ReceiverProfile:
    """Explicit receiver context; no shared knowledge is inferred."""

    name: str
    known_lines: tuple[str, ...] = ()

    @classmethod
    def create(cls, name: str, known_lines: Iterable[str] = ()) -> "ReceiverProfile":
        return cls(name=name, known_lines=tuple(known_lines))


@dataclass(frozen=True, slots=True)
class CompactionResult:
    original: str
    compacted: str
    removed_lines: tuple[str, ...]
    receiver: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def compact_context(text: str, receiver: ReceiverProfile) -> CompactionResult:
    """Remove only full lines the caller explicitly marks as already known."""

    known = {line.strip() for line in receiver.known_lines if line.strip()}
    kept: list[str] = []
    removed: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.strip() in known:
            removed.append(line.strip())
        else:
            kept.append(line)
    return CompactionResult(
        original=text,
        compacted="".join(kept),
        removed_lines=tuple(removed),
        receiver=receiver.name,
    )


def optimize_for_receiver(
    text: str,
    receiver: ReceiverProfile,
    tokenizer: Tokenizer | None = None,
) -> tuple[CompactionResult, Candidate]:
    """Compact explicit shared context, then select a verified candidate."""

    compaction = compact_context(text, receiver)
    return compaction, select_candidate(compaction.compacted, tokenizer=tokenizer)
