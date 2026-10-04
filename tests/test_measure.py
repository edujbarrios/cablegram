from __future__ import annotations

import unittest

from cablegram import Measurement, measure


class FixedTokenizer:
    name = "fixed"

    def count(self, text: str) -> int:
        return 7 if text else 0


class MeasureTests(unittest.TestCase):
    def test_measure_known_text_with_cl100k_base(self) -> None:
        result = measure("Maximum meaning. Minimum tokens.")

        self.assertEqual(
            result,
            Measurement(
                characters=32,
                words=4,
                tokens=6,
                tokenizer="cl100k_base",
            ),
        )

    def test_empty_text_has_zero_counts(self) -> None:
        result = measure("")

        self.assertEqual(result.characters, 0)
        self.assertEqual(result.words, 0)
        self.assertEqual(result.tokens, 0)

    def test_words_are_whitespace_delimited(self) -> None:
        result = measure("one\ttwo\nthree", tokenizer=FixedTokenizer())

        self.assertEqual(result.characters, 13)
        self.assertEqual(result.words, 3)
        self.assertEqual(result.tokens, 7)
        self.assertEqual(result.tokenizer, "fixed")

    def test_measurement_converts_to_dict(self) -> None:
        result = measure("text", tokenizer=FixedTokenizer())

        self.assertEqual(
            result.as_dict(),
            {"characters": 4, "words": 1, "tokens": 7, "tokenizer": "fixed"},
        )


if __name__ == "__main__":
    unittest.main()
