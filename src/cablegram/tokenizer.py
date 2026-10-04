"""Tokenizer boundary and the initial supported implementation."""

from __future__ import annotations

from functools import cached_property
from typing import Protocol

import tiktoken


class Tokenizer(Protocol):
    """Count tokens for a specific, named encoding."""

    @property
    def name(self) -> str:
        """Return the encoding name used for measurement."""

    def count(self, text: str) -> int:
        """Return the number of tokens in text."""


class Cl100kTokenizer:
    """Token counter backed by tiktoken's cl100k_base encoding."""

    @property
    def name(self) -> str:
        return "cl100k_base"

    @cached_property
    def _encoding(self) -> tiktoken.Encoding:
        return tiktoken.get_encoding(self.name)

    def count(self, text: str) -> int:
        return len(self._encoding.encode(text))
