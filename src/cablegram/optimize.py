"""Conservative, auditable deterministic text optimization."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Callable, Iterable

from cablegram.measure import Measurement, measure
from cablegram.tokenizer import Tokenizer


Rule = Callable[[str], str]


@dataclass(frozen=True, slots=True)
class Transformation:
    """One accepted deterministic transformation."""

    rule: str
    before: str
    after: str
    tokens_before: int
    tokens_after: int

    @property
    def token_delta(self) -> int:
        return self.tokens_after - self.tokens_before

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["token_delta"] = self.token_delta
        return data


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    """Auditable result of deterministic optimization."""

    original: str
    optimized: str
    before: Measurement
    after: Measurement
    transformations: tuple[Transformation, ...]

    @property
    def tokens_saved(self) -> int:
        return self.before.tokens - self.after.tokens

    @property
    def reduction(self) -> float:
        if self.before.tokens == 0:
            return 0.0
        return self.tokens_saved / self.before.tokens

    def as_dict(self) -> dict[str, Any]:
        return {
            "original": self.original,
            "optimized": self.optimized,
            "before": self.before.as_dict(),
            "after": self.after.as_dict(),
            "tokens_saved": self.tokens_saved,
            "reduction": self.reduction,
            "transformations": [item.as_dict() for item in self.transformations],
        }


def _map_prose_lines(text: str, transform: Callable[[str], str]) -> str:
    """Apply a line transform outside Markdown fenced code blocks."""

    lines = text.splitlines(keepends=True)
    in_fence = False
    output: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue

        ending = ""
        body = line
        if line.endswith("\r\n"):
            body, ending = line[:-2], "\r\n"
        elif line.endswith("\n") or line.endswith("\r"):
            body, ending = line[:-1], line[-1]
        output.append(transform(body) + ending)
    return "".join(output)


def _normalize_horizontal_whitespace(text: str) -> str:
    def transform(line: str) -> str:
        match = re.match(r"[ \t]*", line)
        prefix = match.group(0) if match else ""
        body = line[len(prefix):]
        return prefix + re.sub(r"[ \t]+", " ", body).rstrip()

    return _map_prose_lines(text, transform)


def _collapse_blank_lines(text: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    in_fence = False
    previous_blank = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            output.append(line)
            previous_blank = False
            continue
        if in_fence:
            output.append(line)
            continue
        is_blank = not line.strip()
        if is_blank and previous_blank:
            continue
        output.append(line)
        previous_blank = is_blank
    return "".join(output)


def _remove_adjacent_duplicate_lines(text: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    previous_key: str | None = None
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            output.append(line)
            previous_key = None
            continue
        if in_fence:
            output.append(line)
            previous_key = None
            continue
        key = line.strip()
        if key and key == previous_key:
            continue
        output.append(line)
        previous_key = key if key else None
    return "".join(output)


_PHRASE_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
    (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
    (re.compile(r"\bplease note that\b", re.IGNORECASE), ""),
    (re.compile(r"\bit is important to note that\b", re.IGNORECASE), ""),
)


def _compact_phrases(text: str) -> str:
    def transform(line: str) -> str:
        match = re.match(r"[ \t]*", line)
        prefix = match.group(0) if match else ""
        result = line[len(prefix):]
        for pattern, replacement in _PHRASE_REPLACEMENTS:
            result = pattern.sub(replacement, result)
        result = re.sub(r" {2,}", " ", result).strip()
        return prefix + result

    return _map_prose_lines(text, transform)


_RULES: tuple[tuple[str, Rule], ...] = (
    ("horizontal-whitespace", _normalize_horizontal_whitespace),
    ("blank-lines", _collapse_blank_lines),
    ("adjacent-duplicate-lines", _remove_adjacent_duplicate_lines),
    ("phrase-compaction", _compact_phrases),
)


def available_rules() -> tuple[str, ...]:
    return tuple(name for name, _ in _RULES)


def optimize(
    text: str,
    tokenizer: Tokenizer | None = None,
    *,
    rules: Iterable[str] | None = None,
) -> OptimizationResult:
    """Apply only deterministic transformations that reduce token count."""

    enabled = set(rules) if rules is not None else set(available_rules())
    unknown = enabled.difference(available_rules())
    if unknown:
        raise ValueError(f"unknown optimization rule(s): {', '.join(sorted(unknown))}")

    current = text
    accepted: list[Transformation] = []
    for name, rule in _RULES:
        if name not in enabled:
            continue
        candidate = rule(current)
        if candidate == current:
            continue
        before = measure(current, tokenizer=tokenizer)
        after = measure(candidate, tokenizer=tokenizer)
        if after.tokens < before.tokens:
            accepted.append(
                Transformation(
                    rule=name,
                    before=current,
                    after=candidate,
                    tokens_before=before.tokens,
                    tokens_after=after.tokens,
                )
            )
            current = candidate

    return OptimizationResult(
        original=text,
        optimized=current,
        before=measure(text, tokenizer=tokenizer),
        after=measure(current, tokenizer=tokenizer),
        transformations=tuple(accepted),
    )
