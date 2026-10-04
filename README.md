# Cablegram

> **Maximum meaning. Minimum tokens.**

**Token-efficient communication for humans and AI agents.**

Created by [Eduardo J. Barrios](https://github.com/edujbarrios), inspired by
[Suffice](https://github.com/edujbarrios/suffice), his open-source project for
finding minimum successful token budgets under task-quality constraints.

In the telegraph era, you paid for every word. In the AI era, we do it again.
Cablegram asks a deceptively difficult question:

> What is the minimum number of tokens required to communicate enough
> information for the receiver to reach the same useful conclusion?

Every token should earn its place.

## The idea

Expert communication makes the idea concrete. A clinical note might say:

```text
The patient is a 67-year-old male with a history of heart failure with reduced
ejection fraction of 30%. During the previous three days he has experienced
progressively worsening dyspnea and orthopnea, gained approximately three
kilograms, and developed bilateral lower-extremity edema.
```

An expert-oriented representation might be:

```text
67M | EF30 | 3d increasing dyspnea/orthopnea | +3kg | BLE edema
```

This is inspiration, not a medical specialization. The underlying problem is
general: reduce communication cost while preserving the information needed for
the receiver and task.

Coding agents offer an immediate example:

```text
I investigated the authentication service and found that the Redis connection
pool appears to have reached its maximum configured capacity. Restarting the
service temporarily resolves the issue, although the connection pool becomes
exhausted again after approximately twenty minutes.
```

```text
auth: Redis pool exhausted -> restart fixes ~20m -> recurs
```

The compact version retains the component, likely cause, temporary remediation,
duration, and recurrence. It must also retain uncertainty where the source is
uncertain. Shorter text that changes the conclusion is a failure.

## Available now

Cablegram currently provides an initial, vendor-neutral communication skill for
AI coding agents: [`skill/SKILL.md`](skill/SKILL.md).

The skill helps an agent produce concise, information-dense messages while
protecting negation, uncertainty, causality, quantities, identifiers, commands,
constraints, and safety information. It requires no model API or runtime
dependency.

To use it, make the skill available through your agent's supported instruction
or skill mechanism. Instruction formats vary, so compatibility is not claimed
for products that have not been tested.

This repository does **not** yet include a tokenizer, CLI, optimizer, semantic
intermediate representation, verifier, benchmark results, or middleware.

## Optimization target

Cablegram's conceptual target is:

```text
useful information transferred / tokens consumed
```

More formally, find the lowest-token representation whose utility for a given
receiver and task remains within an acceptable tolerance of the original. This
is not the same as summarizing, deleting stopwords, or minimizing characters.
The receiver, task, shared context, risk tolerance, and tokenizer all matter.

Long term, Cablegram aims to become a **semantic superoptimizer for minimum
sufficient communication**: generate candidate representations, measure their
actual token cost, and accept one only when appropriate verification supports
its sufficiency.

## Why this is different

Cablegram is organized around useful communication per token, not brevity by
itself. It treats critical one-word distinctions such as `possible` versus
`confirmed`, or `no failure` versus `failure`, as first-class constraints.

Claims must be benchmark-driven. Future measurements will distinguish exact
checks, task-equivalence under a benchmark, heuristic evidence, estimates, and
unknowns. Token reduction alone will never be presented as semantic proof.

## Roadmap

The next phase is measurement: a small, deterministic core and one tokenizer
backend that can report characters, words, and tokens. Later phases may explore
auditable optimization passes, reproducible benchmarks, a small semantic
representation, verification, receiver-aware optimization, history compaction,
and middleware.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the phased plan and
[`docs/VISION.md`](docs/VISION.md) for the research direction. Planned features
are not implemented features.

## Inspiration and acknowledgements

Cablegram was partly inspired by [Suffice](https://github.com/edujbarrios/suffice),
by Eduardo J. Barrios, which explores minimum token budgets under task-success
constraints. Cablegram approaches token efficiency from the communication side:
finding smaller representations while preserving sufficient utility.

[Caveman](https://github.com/JuliusBrussee/caveman) demonstrated the practical
value of reducing unnecessary prose in coding-agent communication. Cablegram
extends the research question toward receiver-aware, task-aware,
tokenizer-aware, and eventually verified representations.

These are acknowledgements of conceptual inspiration; they do not imply code
derivation, endorsement, partnership, or affiliation. See [`NOTICE`](NOTICE).

## Contributing and security

Contributions are welcome. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md) and
follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Report vulnerabilities
using the private process in [`SECURITY.md`](SECURITY.md), not a public issue.

## Citation

Citation metadata is available in [`CITATION.cff`](CITATION.cff).

## License

Copyright 2026 Eduardo J. Barrios. Licensed under the
[Apache License 2.0](LICENSE).
