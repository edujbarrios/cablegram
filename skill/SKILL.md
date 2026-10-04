---
name: cablegram
description: Compress coding-agent messages and handoffs for high information density while preserving task-critical meaning, uncertainty, exact technical details, and safety constraints.
---

# Cablegram

Communicate the minimum sufficient message for the current receiver and task.
Optimize useful information per token, not brevity alone.

## Compose the message

1. Identify the receiver's likely decision or next action.
2. Extract the facts, relationships, and constraints needed for that decision.
3. Remove filler, repeated framing, restatements, and obvious implications.
4. Prefer exact identifiers, values, paths, line numbers, commands, and compact
   causal or temporal structure.
5. Re-read the result against the source before sending it.

Use ordinary concise language by default. Use standard technical abbreviations
when the receiver can reasonably be expected to know them. Use symbols only
when they save tokens for the target tokenizer and remain unambiguous.

## Protect meaning

Never remove or blur a relevant:

- negation, uncertainty, confidence, or assumption;
- cause, dependency, ordering, duration, or recurrence;
- quantity, unit, threshold, version, or comparison;
- filename, path, line number, identifier, command, or exact error;
- constraint, exception, unresolved risk, confirmation requirement, security
  implication, destructive-action warning, or safety warning.

Do not upgrade `possible` to `confirmed`, turn correlation into causation, or
turn a temporary workaround into a fix. When uncertain, retain more context.

## Prefer compact structure

For findings and handoffs, use only fields that carry information. Useful fields
often include `scope`, `cause`, `evidence`, `fix`, `risk`, `status`, and `next`.

Example:

```text
scope: auth/session.ts:118
cause: parallel refresh race
fix: per-session mutex
risk: multi-instance case unresolved
```

Compact prose can encode causal and temporal relationships directly:

```text
auth: Redis pool exhausted -> restart fixes ~20m -> recurs
```

Do not force either format when a sentence, table, code block, or exact command
would be clearer and no more expensive.

## Final check

Before sending, ask:

- Can the receiver make the same useful decision?
- Did any critical qualifier or relationship disappear?
- Is every remaining token doing useful work?

If preservation is uncertain, state that uncertainty or use the fuller form.
