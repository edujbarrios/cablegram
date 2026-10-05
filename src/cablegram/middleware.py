"""Small integration surface for message pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cablegram.candidates import Candidate, select_candidate
from cablegram.context import CompactionResult, ReceiverProfile, optimize_for_receiver
from cablegram.tokenizer import Tokenizer


@dataclass(frozen=True, slots=True)
class MiddlewareResult:
    text: str
    candidate: Candidate
    compaction: CompactionResult | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "candidate": self.candidate.as_dict(),
            "compaction": self.compaction.as_dict() if self.compaction else None,
        }


class CablegramMiddleware:
    """Callable adapter suitable for agent/tool message pipelines."""

    def __init__(
        self,
        *,
        receiver: ReceiverProfile | None = None,
        tokenizer: Tokenizer | None = None,
    ) -> None:
        self.receiver = receiver
        self.tokenizer = tokenizer

    def process(self, text: str) -> MiddlewareResult:
        if self.receiver is None:
            candidate = select_candidate(text, tokenizer=self.tokenizer)
            return MiddlewareResult(text=candidate.text, candidate=candidate)
        compaction, candidate = optimize_for_receiver(
            text,
            self.receiver,
            tokenizer=self.tokenizer,
        )
        return MiddlewareResult(text=candidate.text, candidate=candidate, compaction=compaction)

    def __call__(self, text: str) -> str:
        return self.process(text).text
