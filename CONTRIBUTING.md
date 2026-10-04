# Contributing to Cablegram

Thank you for helping improve token-efficient communication.

## Before you start

Open an issue before investing in a large feature, new dependency, public API,
or architectural change. Small documentation fixes can go directly to a pull
request. Keep each contribution focused on one coherent change.

Cablegram is developed in phases. A roadmap idea is not automatically in scope
for the current phase; see [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Development setup

Cablegram requires Python 3.10 or newer. Clone the repository, create a virtual
environment, and install the project in editable mode:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Run the deterministic test suite with:

```bash
python -m unittest discover -v
```

Build distribution artifacts with `python -m build` when the `build` package is
available. Do not add tools merely to make the repository appear complete.

## Making a contribution

1. Read the README, vision, roadmap, and relevant existing files.
2. Make the smallest coherent change that addresses the issue.
3. Add or update tests when behavior changes.
4. Keep documentation and claims synchronized with implemented behavior.
5. Run all checks documented for the affected area.
6. Explain the change, evidence, limitations, and checks in the pull request.

For skill changes, test realistic coding-agent messages. Check that the output
preserves negation, uncertainty, temporality, causality, quantities, units,
identifiers, paths, commands, constraints, exceptions, and safety warnings.
Avoid tests that assert one exact writing style when multiple representations
are sufficient.

For future optimization passes, document the transformation, conditions under
which it is valid, failure modes, and an explanation format. Passes must be
deterministic unless explicitly labeled otherwise.

For future benchmark cases, include the receiver, task, input, critical facts,
expected checks, and measurement provenance. Do not submit invented results or
claim broad equivalence from a narrow case.

## Contribution terms

By submitting a contribution, you agree that it is licensed under the
[Apache License 2.0](LICENSE), consistent with Section 5 of that license. Only
submit work you have the right to contribute. Preserve attribution and identify
third-party material and its license.

All participants must follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
Report security vulnerabilities through [`SECURITY.md`](SECURITY.md), not in a
public issue.
