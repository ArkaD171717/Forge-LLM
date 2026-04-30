"""Repo-to-context ingestion, re-exported from qwen3-repo."""

from qwen3_repo import (
    AgentRunResult,
    ContextBudget,
    OpenAIClient,
    RankedFile,
    detect_ollama_vision_capability,
    detect_vision_needs,
    estimate_tokens,
    ingest_repo,
    rank_files,
    run_agent,
)

__all__ = [
    "ingest_repo",
    "estimate_tokens",
    "ContextBudget",
    "rank_files",
    "RankedFile",
    "detect_vision_needs",
    "detect_ollama_vision_capability",
    "OpenAIClient",
    "run_agent",
    "AgentRunResult",
]
