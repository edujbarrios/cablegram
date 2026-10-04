# Roadmap

Cablegram develops in evidence-building phases. Each phase should remain small,
tested, and honest about what it establishes.

## Phase 1: open-source foundation (current)

- Establish Apache-2.0 licensing, attribution, contribution, conduct, security,
  citation, vision, and roadmap documents.
- Publish a usable communication skill for coding agents.
- Make no optimizer or benchmark-performance claims.

## Phase 2: measurement foundation

- Add a minimal Python core and `cablegram measure` command.
- Report characters, words, and tokens with clear definitions.
- Support one tokenizer behind an interface that can evolve.
- Add deterministic tests and minimal CI.

## Phase 3: deterministic optimization MVP

- Add conservative, auditable transformations such as filler elimination,
  whitespace normalization, and exact duplicate removal.
- Explain every transformation and measure its effect.
- Describe outputs as deterministic optimization, not semantic equivalence.

## Phase 4: benchmark harness

- Define a small set of high-quality cases with receiver, task, critical facts,
  expected checks, token counts, and pass/fail outcomes.
- Store enough provenance to reproduce every result.

## Phase 5: semantic representation experiment

- Explore a deliberately narrow, inspectable representation for facts,
  relations, negation, uncertainty, quantities, time, and constraints.
- Mark the interface experimental and document its limits.

## Phase 6: candidate generation

- Produce multiple representations and measure actual tokenizer cost.
- Never select the smallest candidate solely because it is smallest.

## Phase 7: verification

- Combine invariant checks, structured reconstruction, entailment checks, and
  task-based evaluation as appropriate.
- Keep model-dependent evaluation optional and record its provenance.

## Phase 8: receiver-aware optimization

- Test how receiver and task context change minimum sufficient representations.
- Replace assumed shared knowledge with measured outcomes.

## Phase 9: context compaction

- Explore removal of information that no longer needs retransmission while
  preserving what future tasks require.

## Phase 10: middleware and proxy interfaces

- Integrate verified optimization into agent and tool pipelines only after the
  message-level system demonstrates reproducible value.

Roadmap order may change when evidence warrants it. Planned work is not a claim
of availability.
