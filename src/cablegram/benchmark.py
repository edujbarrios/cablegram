"""Reproducible benchmark harness for deterministic optimization."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from cablegram.candidates import select_candidate
from cablegram.measure import measure
from cablegram.tokenizer import Tokenizer


@dataclass(frozen=True, slots=True)
class BenchmarkCaseResult:
    name: str
    passed: bool
    input_tokens: int
    output_tokens: int
    required_substrings_present: bool
    invariants_preserved: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "tokens_saved": self.input_tokens - self.output_tokens,
            "required_substrings_present": self.required_substrings_present,
            "invariants_preserved": self.invariants_preserved,
        }


@dataclass(frozen=True, slots=True)
class BenchmarkReport:
    benchmark: str
    passed: bool
    cases: tuple[BenchmarkCaseResult, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "benchmark": self.benchmark,
            "passed": self.passed,
            "cases": [case.as_dict() for case in self.cases],
            "total_tokens_saved": sum(case.input_tokens - case.output_tokens for case in self.cases),
        }


def _contains(text: str, required: str) -> bool:
    return " ".join(required.casefold().split()) in " ".join(text.casefold().split())


def run_benchmark_document(
    document: Mapping[str, Any],
    tokenizer: Tokenizer | None = None,
) -> BenchmarkReport:
    """Run a versioned deterministic benchmark document."""

    benchmark = str(document.get("benchmark", "unnamed"))
    results: list[BenchmarkCaseResult] = []
    for raw_case in document.get("cases", ()):
        name = str(raw_case["name"])
        source = str(raw_case["input"])
        required = tuple(str(value) for value in raw_case.get("required_substrings", ()))
        candidate = select_candidate(source, tokenizer=tokenizer)
        required_ok = all(_contains(candidate.text, value) for value in required)
        before = measure(source, tokenizer=tokenizer)
        passed = candidate.verification.passed and required_ok and candidate.measurement.tokens <= before.tokens
        results.append(
            BenchmarkCaseResult(
                name=name,
                passed=passed,
                input_tokens=before.tokens,
                output_tokens=candidate.measurement.tokens,
                required_substrings_present=required_ok,
                invariants_preserved=candidate.verification.passed,
            )
        )
    return BenchmarkReport(
        benchmark=benchmark,
        passed=bool(results) and all(case.passed for case in results),
        cases=tuple(results),
    )


def run_benchmark(path: str | Path, tokenizer: Tokenizer | None = None) -> BenchmarkReport:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return run_benchmark_document(data, tokenizer=tokenizer)
