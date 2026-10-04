from __future__ import annotations

from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from cablegram.cli import main


class CliTests(unittest.TestCase):
    def test_measure_file_as_json(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory, "message.txt")
            path.write_text("Maximum meaning. Minimum tokens.", encoding="utf-8")
            output = StringIO()

            exit_code = main(["measure", str(path), "--json"], stdout=output)

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(output.getvalue()),
            {
                "characters": 32,
                "words": 4,
                "tokens": 6,
                "tokenizer": "cl100k_base",
            },
        )

    def test_measure_stdin_as_text(self) -> None:
        output = StringIO()

        exit_code = main(
            ["measure", "-"],
            stdin=StringIO("one two"),
            stdout=output,
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            output.getvalue(),
            "characters: 7\nwords:      2\ntokens:     2\ntokenizer:  cl100k_base\n",
        )

    def test_measure_preserves_file_line_endings(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory, "message.txt")
            path.write_bytes(b"one\r\ntwo")
            output = StringIO()

            exit_code = main(["measure", str(path), "--json"], stdout=output)

        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output.getvalue())["characters"], 8)


if __name__ == "__main__":
    unittest.main()
