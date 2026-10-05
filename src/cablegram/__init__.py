"""Token-efficient communication with conservative deterministic safeguards."""

from cablegram.benchmark import BenchmarkReport, run_benchmark, run_benchmark_document
from cablegram.candidates import Candidate, generate_candidates, select_candidate
from cablegram.context import CompactionResult, ReceiverProfile, compact_context, optimize_for_receiver
from cablegram.measure import Measurement, measure
from cablegram.middleware import CablegramMiddleware, MiddlewareResult
from cablegram.optimize import OptimizationResult, Transformation, available_rules, optimize
from cablegram.semantic import Fact, SemanticMessage
from cablegram.tokenizer import Cl100kTokenizer, Tokenizer
from cablegram.verify import Invariants, VerificationResult, extract_invariants, verify

__all__ = [
    "BenchmarkReport",
    "CablegramMiddleware",
    "Candidate",
    "Cl100kTokenizer",
    "CompactionResult",
    "Fact",
    "Invariants",
    "Measurement",
    "MiddlewareResult",
    "OptimizationResult",
    "ReceiverProfile",
    "SemanticMessage",
    "Tokenizer",
    "Transformation",
    "VerificationResult",
    "available_rules",
    "compact_context",
    "extract_invariants",
    "generate_candidates",
    "measure",
    "optimize",
    "optimize_for_receiver",
    "run_benchmark",
    "run_benchmark_document",
    "select_candidate",
    "verify",
]
__version__ = "0.2.0"
