"""Cablegram command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence, TextIO

from cablegram.measure import Measurement, measure


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cablegram",
        description="Measure communication cost before optimizing it.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    measure_parser = subparsers.add_parser(
        "measure",
        help="count characters, words, and cl100k_base tokens",
    )
    measure_parser.add_argument("input", help="UTF-8 text file, or - for stdin")
    measure_parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )
    return parser


def _read_text(source: str, stdin: TextIO) -> str:
    if source == "-":
        return stdin.read()
    return Path(source).read_bytes().decode("utf-8")


def _format_measurement(result: Measurement, as_json: bool) -> str:
    if as_json:
        return json.dumps(result.as_dict(), sort_keys=True)
    return "\n".join(
        (
            f"characters: {result.characters}",
            f"words:      {result.words}",
            f"tokens:     {result.tokens}",
            f"tokenizer:  {result.tokenizer}",
        )
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    input_stream = stdin or sys.stdin
    output_stream = stdout or sys.stdout

    try:
        text = _read_text(args.input, input_stream)
    except (OSError, UnicodeError) as error:
        parser.error(f"cannot read {args.input!r}: {error}")

    result = measure(text)
    print(_format_measurement(result, args.json), file=output_stream)
    return 0
