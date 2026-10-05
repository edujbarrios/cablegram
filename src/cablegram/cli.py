"""Cablegram command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence, TextIO

from cablegram.benchmark import run_benchmark
from cablegram.candidates import select_candidate
from cablegram.context import ReceiverProfile, compact_context
from cablegram.measure import Measurement, measure
from cablegram.verify import verify


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cablegram",
        description="Measure and conservatively optimize token-efficient communication.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    measure_parser = subparsers.add_parser(
        "measure",
        help="count characters, words, and cl100k_base tokens",
    )
    measure_parser.add_argument("input", help="UTF-8 text file, or - for stdin")
    measure_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    optimize_parser = subparsers.add_parser(
        "optimize",
        help="select the smallest deterministic candidate that preserves invariants",
    )
    optimize_parser.add_argument("input", help="UTF-8 text file, or - for stdin")
    optimize_parser.add_argument("--json", action="store_true", help="include metrics and verification")

    verify_parser = subparsers.add_parser(
        "verify",
        help="check whether a candidate preserves deterministic source invariants",
    )
    verify_parser.add_argument("source", help="source UTF-8 text file")
    verify_parser.add_argument("candidate", help="candidate UTF-8 text file")
    verify_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="run a deterministic benchmark document",
    )
    benchmark_parser.add_argument("input", help="benchmark JSON file")
    benchmark_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    compact_parser = subparsers.add_parser(
        "compact",
        help="remove exact lines explicitly declared known by a receiver",
    )
    compact_parser.add_argument("input", help="UTF-8 text file, or - for stdin")
    compact_parser.add_argument("--known", required=True, help="UTF-8 file containing one known line per line")
    compact_parser.add_argument("--receiver", default="receiver", help="receiver profile name")
    compact_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
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


def _json(data: Any) -> str:
    return json.dumps(data, sort_keys=True)


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
        if args.command == "measure":
            text = _read_text(args.input, input_stream)
            print(_format_measurement(measure(text), args.json), file=output_stream)
            return 0

        if args.command == "optimize":
            text = _read_text(args.input, input_stream)
            candidate = select_candidate(text)
            print(
                _json(candidate.as_dict()) if args.json else candidate.text,
                file=output_stream,
                end="\n" if args.json or not candidate.text.endswith("\n") else "",
            )
            return 0

        if args.command == "verify":
            source = _read_text(args.source, input_stream)
            candidate_text = _read_text(args.candidate, input_stream)
            result = verify(source, candidate_text)
            if args.json:
                print(_json(result.as_dict()), file=output_stream)
            else:
                print("PASS" if result.passed else "FAIL", file=output_stream)
                if result.missing:
                    for category, values in result.missing.items():
                        print(f"missing {category}: {', '.join(values)}", file=output_stream)
            return 0 if result.passed else 1

        if args.command == "benchmark":
            report = run_benchmark(args.input)
            if args.json:
                print(_json(report.as_dict()), file=output_stream)
            else:
                print(f"benchmark: {report.benchmark}", file=output_stream)
                print(f"status: {'PASS' if report.passed else 'FAIL'}", file=output_stream)
                for case in report.cases:
                    print(
                        f"{case.name}: {'PASS' if case.passed else 'FAIL'} "
                        f"({case.input_tokens} -> {case.output_tokens} tokens)",
                        file=output_stream,
                    )
            return 0 if report.passed else 1

        if args.command == "compact":
            text = _read_text(args.input, input_stream)
            known_text = Path(args.known).read_text(encoding="utf-8")
            profile = ReceiverProfile.create(args.receiver, known_text.splitlines())
            result = compact_context(text, profile)
            print(
                _json(result.as_dict()) if args.json else result.compacted,
                file=output_stream,
                end="\n" if args.json or not result.compacted.endswith("\n") else "",
            )
            return 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, KeyError) as error:
        parser.error(str(error))

    parser.error(f"unsupported command: {args.command}")
    return 2
