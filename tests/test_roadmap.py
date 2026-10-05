from __future__ import annotations

import re
import unittest

from cablegram.benchmark import run_benchmark_document
from cablegram.candidates import generate_candidates, select_candidate
from cablegram.context import ReceiverProfile, compact_context, optimize_for_receiver
from cablegram.middleware import CablegramMiddleware
from cablegram.optimize import optimize
from cablegram.semantic import Fact, SemanticMessage
from cablegram.verify import verify


class WordTokenizer:
    name = "words"

    def count(self, text: str) -> int:
        return len(re.findall(r"\S+", text))


class CharacterTokenizer:
    name = "characters"

    def count(self, text: str) -> int:
        return len(text)


class RoadmapTests(unittest.TestCase):
    def test_optimizer_is_auditable_and_only_accepts_savings(self) -> None:
        source = (
            "Please note that in order to reproduce, run 4 instances.\n"
            "Please note that in order to reproduce, run 4 instances.\n"
        )
        result = optimize(source, tokenizer=WordTokenizer())

        self.assertLess(result.after.tokens, result.before.tokens)
        self.assertGreater(result.tokens_saved, 0)
        self.assertTrue(result.transformations)
        self.assertTrue(all(item.tokens_after < item.tokens_before for item in result.transformations))
        self.assertIn("4", result.optimized)

    def test_optimizer_does_not_modify_fenced_code(self) -> None:
        source = "Please note that this is prose.\n```python\nvalue  =  50\n\n\n```\n"
        result = optimize(source, tokenizer=CharacterTokenizer())

        self.assertIn("value  =  50\n\n\n```", result.optimized)
        self.assertIn("```python", result.optimized)

    def test_verifier_detects_missing_critical_surface_facts(self) -> None:
        source = "Do not deploy. Root cause unconfirmed. Pool max 50 at src/auth/session.ts."
        candidate = "Do not deploy. Root cause unconfirmed at src/auth/session.ts."
        result = verify(source, candidate)

        self.assertFalse(result.passed)
        self.assertIn("numbers", result.missing)
        self.assertEqual(result.missing["numbers"], ("50",))

    def test_candidate_selection_requires_verification(self) -> None:
        source = "Please note that in order to retry, use 4 workers. Do not use 5 workers."
        candidates = generate_candidates(source, tokenizer=WordTokenizer())
        selected = select_candidate(source, tokenizer=WordTokenizer())

        self.assertGreaterEqual(len(candidates), 2)
        self.assertTrue(selected.verification.passed)
        self.assertIn("4", selected.text)
        self.assertIn("5", selected.text)
        self.assertIn("not", selected.text.casefold())

    def test_semantic_message_round_trip_is_explicit(self) -> None:
        message = SemanticMessage.from_facts(
            [
                Fact(
                    subject="redis pool",
                    predicate="reaches",
                    object="max 50",
                    qualifiers=("during parallel refresh",),
                    confidence="observed",
                )
            ]
        )
        rebuilt = SemanticMessage.from_dict(message.to_dict())

        self.assertEqual(rebuilt, message)
        self.assertIn("confidence=observed", rebuilt.render())

    def test_receiver_compaction_removes_only_declared_exact_lines(self) -> None:
        source = "service: auth\nimpact: HTTP 503\nnext: reproduce with 4 instances\n"
        receiver = ReceiverProfile.create("backend", ["service: auth"])
        result = compact_context(source, receiver)

        self.assertEqual(result.removed_lines, ("service: auth",))
        self.assertNotIn("service: auth", result.compacted)
        self.assertIn("HTTP 503", result.compacted)

    def test_receiver_optimization_and_middleware(self) -> None:
        source = "known: auth service\nPlease note that in order to retry, use 4 workers.\n"
        receiver = ReceiverProfile.create("backend", ["known: auth service"])
        compaction, candidate = optimize_for_receiver(source, receiver, tokenizer=WordTokenizer())
        middleware = CablegramMiddleware(receiver=receiver, tokenizer=WordTokenizer())

        self.assertEqual(compaction.removed_lines, ("known: auth service",))
        self.assertTrue(candidate.verification.passed)
        self.assertEqual(middleware(source), candidate.text)

    def test_benchmark_harness_reproduces_checks(self) -> None:
        document = {
            "benchmark": "unit-v1",
            "cases": [
                {
                    "name": "handoff",
                    "input": "Please note that in order to retry, use 4 workers. Do not use 5 workers.",
                    "required_substrings": ["4 workers", "Do not use 5 workers"],
                }
            ],
        }
        report = run_benchmark_document(document, tokenizer=WordTokenizer())

        self.assertTrue(report.passed)
        self.assertGreater(report.cases[0].input_tokens, report.cases[0].output_tokens)


if __name__ == "__main__":
    unittest.main()
