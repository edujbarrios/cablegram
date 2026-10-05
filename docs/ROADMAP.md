# Roadmap

Cablegram develops in evidence-building phases. The original ten-phase roadmap is now implemented at an intentionally conservative, dependency-light scope. “Complete” below means the repository contains a tested interface for the phase; it does **not** mean semantic equivalence has been solved in general.

## Phase 1: open-source foundation — complete

- Apache-2.0 licensing, attribution, contribution, conduct, security, citation, vision, and roadmap documents.
- A vendor-neutral communication skill for coding agents.
- Pilot results kept separate from general claims.

## Phase 2: measurement foundation — complete

- Python API and `cablegram measure` CLI.
- Character, whitespace-delimited word, and `cl100k_base` token counts.
- Tokenizer protocol, deterministic tests, and CI.

## Phase 3: deterministic optimization MVP — complete

- Conservative rules for horizontal whitespace, repeated blank lines, adjacent exact duplicate lines, and a small allowlist of verbose phrases.
- Markdown fenced code is not rewritten.
- A rule is accepted only when it actually reduces token count.
- Every accepted transformation records before/after text and token counts.

## Phase 4: benchmark harness — complete

- Versioned JSON benchmark format with source text and required substrings.
- Reproducible token measurement and pass/fail reports.
- `benchmarks/deterministic_v1.json` is the first executable benchmark; the older agent handoff remains a pilot artifact.

## Phase 5: semantic representation experiment — complete

- `Fact` and `SemanticMessage` provide a deliberately narrow, inspectable representation.
- Facts are caller-authored; Cablegram does not pretend to infer semantics from arbitrary prose.
- Qualifiers and confidence are explicit and round-trippable.

## Phase 6: candidate generation — complete

- Cablegram generates the original, per-rule candidates, and an all-rules candidate.
- Candidates are measured with the actual tokenizer.
- Selection never uses size alone: a candidate must pass deterministic invariant checks.

## Phase 7: verification — complete for deterministic scope

- Surface invariants cover numbers, negation, uncertainty, constraints, paths/URLs, and backtick identifiers.
- Selection rejects candidates that drop a protected invariant.
- Model-based entailment remains optional future research rather than a hidden runtime dependency.

## Phase 8: receiver-aware optimization — complete for explicit context

- `ReceiverProfile` makes shared context explicit.
- No receiver knowledge is inferred automatically.
- Receiver-aware optimization compacts only caller-declared known lines before verified candidate selection.

## Phase 9: context compaction — complete for exact known context

- Exact full lines declared as already known can be removed with an audit trail.
- Unknown or partially matching lines are retained.

## Phase 10: middleware and proxy interfaces — complete

- `CablegramMiddleware` is a small callable adapter for agent/tool pipelines.
- It supports plain deterministic selection or receiver-aware compaction.
- Network proxies and vendor-specific integrations are intentionally outside the core package.

## What remains research, not roadmap debt

The repository now implements the roadmap as a usable alpha. Open research questions remain: learned candidate generation, semantic entailment, task-based utility measurement, receiver knowledge estimation, and large-scale benchmark evidence. Those are extensions, not claims made by the current deterministic system.
