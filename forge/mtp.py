"""MTP speculative decoding helpers, re-exported from qwen3.6-mtp."""

from qwen3_6_mtp import (
    Objective,
    UseCase,
    quick_crossover,
    recommend,
    sglang_mtp_command,
    vllm_mtp_command,
)

__all__ = [
    "recommend",
    "quick_crossover",
    "vllm_mtp_command",
    "sglang_mtp_command",
    "UseCase",
    "Objective",
]
