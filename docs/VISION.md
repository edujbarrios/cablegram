# Vision

Cablegram investigates minimum sufficient communication: the least expensive
representation that still lets a particular receiver complete a particular
task to an acceptable standard.

## The research question

The objective is to minimize tokens subject to a utility-preservation
constraint. Utility is contextual rather than universal. It depends on the
message, receiver, task, shared context, risk tolerance, target model, and
target tokenizer.

This framing separates Cablegram from systems that optimize only prose length.
A shorter message can be worse if it loses a negation, changes confidence,
breaks a causal relation, drops a unit, or obscures an operational warning.

## Design principles

- Preserve task-relevant meaning before reducing cost.
- Measure tokens with explicit provenance rather than infer them from length.
- Keep transformations inspectable and explainable.
- Distinguish verification from similarity.
- Adapt representations to receivers only when assumptions are explicit.
- Earn performance claims with reproducible benchmarks.
- Keep deterministic, offline use possible where practical.

## Long-term shape

A mature Cablegram may resemble a compiler superoptimizer. It would analyze a
message, form a deliberately small semantic representation, generate candidate
transformations, measure candidates against a target tokenizer, and verify that
the chosen representation remains sufficient for the receiver and task.

Potential applications include agent responses, agent-to-agent handoffs, tool
results, logs, test output, diffs, retrieval context, conversation history,
technical documentation, and API responses. The project remains
domain-independent; medicine is an illustrative source of expert shorthand,
not the product domain.

## Scientific boundaries

Cablegram will not treat embedding similarity as proof of preservation or token
savings as proof of success. Results should state whether preservation is
exactly checked, task-equivalent under a stated benchmark, heuristic, estimated,
or unknown. No universal quality or savings claim is justified without evidence
across the relevant receiver, task, and tokenizer conditions.

The current repository contains only the open-source foundation and initial
communication skill. The optimizer described here is a research direction.
