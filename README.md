# Cablegram

> **Maximum meaning. Minimum tokens.**

**Token-efficient communication for humans and AI agents.**

Created by [Eduardo J. Barrios](https://github.com/edujbarrios), inspired by [Suffice](https://github.com/edujbarrios/suffice), his open-source project for finding minimum successful token budgets under task-quality constraints.

In the telegraph era, you paid for every word. In the AI era, token cost makes the same question useful again:

> What is the smallest representation that still gives a particular receiver enough information to complete a particular task?

Cablegram treats token reduction as an optimization problem with preservation constraints, not as permission to delete meaning.

## Example

A verbose incident handoff:

```text
I investigated the authentication service and found that the Redis connection
pool appears to have reached its maximum configured capacity. Restarting the
service temporarily resolves the issue, although the connection pool becomes
exhausted again after approximately twenty minutes.
```

A compact expert-oriented representation:

```text
auth: Redis pool appears exhausted -> restart fixes ~20m -> recurs
```

The compact version is useful only if it preserves what the receiver needs. `appears`, `~20m`, and `recurs` are not decoration: uncertainty, quantity, and recurrence can change the conclusion.

## Install

Cablegram requires Python 3.10+.

```bash
python -m pip install -e .
```

The core runtime dependency is `tiktoken`; the default tokenizer is `cl100k_base`.

## CLI

Measure exact input cost:

```bash
cablegram measure examples/message.txt
```

```text
characters: 33
words:      4
tokens:     6
tokenizer:  cl100k_base
```

Use `-` for stdin and `--json` for machine-readable output:

```bash
printf 'Maximum meaning. Minimum tokens.' | cablegram measure - --json
```

Select the smallest deterministic candidate that passes Cablegram's invariant checks:

```bash
cablegram optimize examples/message.txt
cablegram optimize examples/message.txt --json
```

Compare a candidate with its source:

```bash
cablegram verify source.txt candidate.txt
```

Run an executable benchmark:

```bash
cablegram benchmark benchmarks/deterministic_v1.json
```

Compact context that a receiver is explicitly known to already have:

```bash
cablegram compact handoff.txt --known receiver-known-lines.txt --receiver backend
```

## Python API

Measurement remains the smallest API:

```python
from cablegram import measure

result = measure("Maximum meaning. Minimum tokens.")
print(result.tokens)  # 6 with cl100k_base
```

Deterministic optimization is auditable:

```python
from cablegram import optimize

result = optimize("Please note that in order to retry, restart the worker.")
print(result.optimized)
print(result.tokens_saved)
for change in result.transformations:
    print(change.rule, change.tokens_before, "->", change.tokens_after)
```

Verified candidate selection adds a preservation gate:

```python
from cablegram import select_candidate

candidate = select_candidate("Do not deploy. Pool max 50. Root cause unconfirmed.")
assert candidate.verification.passed
print(candidate.text)
```

Receiver context is explicit rather than inferred:

```python
from cablegram import CablegramMiddleware, ReceiverProfile

receiver = ReceiverProfile.create("backend", known_lines=["service: auth"])
compress = CablegramMiddleware(receiver=receiver)
message = compress("service: auth\nnext: reproduce with 4 instances\n")
```

## What the optimizer does

The deterministic optimizer is intentionally small. It can normalize horizontal whitespace, collapse excessive blank lines, remove adjacent exact duplicate lines, and compact a short allowlist of verbose phrases. Markdown fenced code is not rewritten. A transformation is committed only if the configured tokenizer reports an actual token reduction.

Candidate generation evaluates the original text, each rule independently, and all rules together. Selection chooses the lowest-token candidate that preserves deterministic surface invariants extracted from the source:

- numbers and percentages;
- negation;
- uncertainty language;
- constraint language;
- paths, URLs, and backtick identifiers.

These checks are conservative guards, **not semantic equivalence proofs**. Equivalent paraphrases can fail a surface check, and text can preserve every checked invariant while still changing some unmodeled meaning.

## Optimization model

Let `m0` be the original message, `m` a candidate, `r` the receiver, `t` the task, and `τ` the tokenizer. Token cost is:

$$
T_{\tau}(m) = |\tau(m)|
$$

For a non-empty original message, token reduction is:

$$
\rho(m; m_0) = 1 - \frac{T_{\tau}(m)}{T_{\tau}(m_0)}, \qquad T_{\tau}(m_0) > 0
$$

The research objective is minimum token cost subject to task utility staying within tolerance:

$$
m^{\star} = \underset{m \in \mathcal{C}(m_0)}{\arg\min}\; T_{\tau}(m)
$$

subject to

$$
U(m,r,t) \ge U(m_0,r,t) - \varepsilon
$$

and, for protected deterministic invariants `P`:

$$
P(m_0) \subseteq P(m)
$$

A utility-per-token quantity can be useful when utility is actually measurable:

$$
E(m,r,t) = \frac{U(m,r,t)}{T_{\tau}(m)}, \qquad T_{\tau}(m) > 0
$$

The important distinction is that the current package can measure `Tτ` and enforce selected members of `P`; it does **not** claim to estimate general `U`. The formulas describe both the implemented deterministic gate and the broader research target without conflating them.

## Benchmarking

`benchmarks/deterministic_v1.json` is executable by the benchmark harness. Each case contains source text and substrings that must remain explicit. A case passes only when required substrings remain present, deterministic invariants pass, and the selected candidate uses no more tokens than the source.

The earlier [`benchmarks/agent_handoff_v1.json`](benchmarks/agent_handoff_v1.json) remains a pilot artifact: two agent outputs, one run per condition, with a manual ten-fact presence check. It showed 126 -> 113 tokens while retaining 10/10 explicitly scored facts. That is a single-task observation, not a general reduction rate or semantic proof.

## Semantic representation

`Fact` and `SemanticMessage` provide a deliberately narrow experiment for structured facts, qualifiers, and confidence. The caller supplies the facts; Cablegram does not silently infer a knowledge graph from arbitrary prose.

This boundary is intentional: explicit structure is inspectable and round-trippable, while general semantic extraction would require stronger assumptions and evaluation.

## Receiver-aware context and middleware

`ReceiverProfile` can declare exact lines already known to a receiver. Context compaction removes only those full lines and records what was removed. Cablegram never guesses what a receiver knows.

`CablegramMiddleware` exposes the same behavior as a callable adapter for agent or tool pipelines. Vendor-specific proxies and network integrations stay outside the dependency-light core.

## Communication skill

The repository also includes a vendor-neutral instruction skill at [`skill/SKILL.md`](skill/SKILL.md). It helps coding agents write concise, information-dense messages while protecting negation, uncertainty, causality, quantities, identifiers, commands, constraints, and safety information. It requires no model API or runtime dependency.

## Roadmap status

The original ten implementation phases now have conservative, tested interfaces in the repository: foundation, measurement, deterministic optimization, benchmark harness, semantic representation, candidate generation, verification, receiver-aware optimization, context compaction, and middleware.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the exact completion criteria and [`docs/VISION.md`](docs/VISION.md) for the research direction. Learned generation, semantic entailment, task-based utility estimation, and large-scale empirical validation remain open research rather than hidden claims.

## Development

Run the test suite with:

```bash
python -m unittest discover -v
```

CI runs on Python 3.10 and 3.12.

## Inspiration and acknowledgements

Cablegram was partly inspired by [Suffice](https://github.com/edujbarrios/suffice), by Eduardo J. Barrios, which explores minimum token budgets under task-success constraints. Cablegram approaches token efficiency from the communication side: finding smaller representations while preserving sufficient utility.

[Caveman](https://github.com/JuliusBrussee/caveman) demonstrated the practical value of reducing unnecessary prose in coding-agent communication. Cablegram extends the research question toward receiver-aware, task-aware, tokenizer-aware, and verifiable representations.

These acknowledgements do not imply code derivation, endorsement, partnership, or affiliation. See [`NOTICE`](NOTICE).

## Contributing and security

Contributions are welcome. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md) and follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Report vulnerabilities using the private process in [`SECURITY.md`](SECURITY.md), not a public issue.

## Citation

Citation metadata is available in [`CITATION.cff`](CITATION.cff).

## License

Copyright 2026 Eduardo J. Barrios. Licensed under the [Apache License 2.0](LICENSE).
