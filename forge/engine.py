"""Integration layer that chains session, MTP, and context into one workflow."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

from qwen3_6_mtp import Objective, UseCase, recommend
from qwen3_6_mtp.types import MtpRecommendation
from qwen3_repo import ContextBudget, estimate_tokens
from qwen3_repo.ingester import (
    build_dependency_graph,
    compute_ordering,
    discover_files,
    format_context_pack,
    ingest_repo,
)
from qwen_think import ThinkingMode, ThinkingSession

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment,misc]

logger = logging.getLogger("forge.engine")


class ForgeEngine:
    """End-to-end inference engine for Qwen3.6 reasoning models.

    Chains MTP recommendation, repo context ingestion, and thinking
    session management into a single configure-once workflow.
    """

    def __init__(
        self,
        model: str = "Qwen3.6-27B",
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "EMPTY",
        *,
        backend: Optional[str] = None,
        gpu_id: Optional[str] = None,
        use_case: UseCase = UseCase.SINGLE_USER,
        objective: Objective = Objective.MINIMIZE_LATENCY,
        budget: int = 200_000,
        auto_route: bool = True,
        force_thinking: bool = False,
        system_prompt: Optional[str] = None,
    ) -> None:
        if OpenAI is None:
            raise ImportError(
                "ForgeEngine requires the openai package. "
                "Install with: pip install forge-infer[openai]"
            )

        if "/" in model:
            self._model_hf = model
            self._model_short = model.split("/")[-1]
        else:
            self._model_short = model
            self._model_hf = f"Qwen/{model}"

        self._base_url = base_url
        self._budget_total = budget
        self._system_prompt = system_prompt
        self._context_pack: Optional[str] = None
        self._context_budget: Optional[ContextBudget] = None
        self._context_files: int = 0
        self._context_tokens: int = 0

        client = OpenAI(base_url=base_url, api_key=api_key)
        self._session = ThinkingSession(
            client=client,
            model=self._model_hf,
            backend=backend,
            budget=budget,
            auto_route=auto_route,
            force_thinking=force_thinking,
        )

        if system_prompt:
            self._session.add_message("system", system_prompt)

        self._mtp_rec: Optional[MtpRecommendation] = None
        if gpu_id:
            self._mtp_rec = recommend(
                use_case=use_case,
                objective=objective,
                gpu_id=gpu_id,
                model=self._model_short,
            )
            for w in self._mtp_rec.warnings:
                logger.warning("MTP: %s", w)

    @property
    def mtp_recommendation(self) -> Optional[MtpRecommendation]:
        return self._mtp_rec

    @property
    def session(self) -> ThinkingSession:
        return self._session

    @property
    def context_pack(self) -> Optional[str]:
        return self._context_pack

    @property
    def context_budget(self) -> Optional[ContextBudget]:
        return self._context_budget

    def ingest(
        self,
        repo_url: str,
        *,
        branch: Optional[str] = None,
        clone_depth: Optional[int] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Clone and ingest a remote repo into the session context."""
        pack, files, ctx_budget = ingest_repo(
            repo_url,
            model=self._model_short,
            branch=branch,
            clone_depth=clone_depth,
            max_tokens=max_tokens,
        )
        self._apply_context(pack, len(files), ctx_budget)
        return pack

    def ingest_local(
        self,
        repo_path: str,
        *,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Ingest a local directory into the session context."""
        root = Path(repo_path).resolve()
        ctx_budget = ContextBudget(model=self._model_short)
        if max_tokens:
            ctx_budget.pack_budget = max_tokens

        files = discover_files(root)
        dep_graph = build_dependency_graph(files)
        ordered = compute_ordering(files, dep_graph, ctx_budget)
        pack = format_context_pack(ordered)

        self._apply_context(pack, len(ordered), ctx_budget)
        return pack

    def set_context(self, context_pack: str) -> None:
        """Inject a pre-computed context pack into the session."""
        tokens = estimate_tokens(context_pack)
        self._context_pack = context_pack
        self._context_tokens = tokens
        self._context_files = 0
        self._context_budget = None
        self._session.add_message("system", context_pack)

    def chat(
        self,
        message: str,
        *,
        mode: Optional[ThinkingMode] = None,
        system: Optional[str] = None,
        max_tokens: int = 8192,
        stream: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Send a message and get a response."""
        return self._session.chat(
            message,
            mode=mode,
            system=system,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs,
        )

    def status(self) -> dict[str, Any]:
        """Summary of engine state."""
        budget_st = self._session.budget_status

        result: dict[str, Any] = {
            "model": self._model_short,
            "model_hf": self._model_hf,
            "backend": str(self._session.backend),
            "base_url": self._base_url,
            "thinking_mode": self._session.thinking_mode.value,
            "budget": {
                "total": budget_st.total_tokens,
                "used": budget_st.used_tokens,
                "available": budget_st.available_tokens,
                "action": budget_st.action.value,
            },
            "messages": len(self._session.messages),
        }

        if self._mtp_rec:
            result["mtp"] = {
                "enable": self._mtp_rec.enable,
                "num_speculative_tokens": self._mtp_rec.num_speculative_tokens,
                "expected_gain": self._mtp_rec.expected_gain,
                "warnings": self._mtp_rec.warnings,
                "vllm_command": self._mtp_rec.vllm_command,
                "sglang_command": self._mtp_rec.sglang_command,
            }

        if self._context_pack:
            result["context"] = {
                "tokens": self._context_tokens,
                "files": self._context_files,
            }

        return result

    def _apply_context(
        self,
        pack: str,
        file_count: int,
        ctx_budget: ContextBudget,
    ) -> None:
        self._context_pack = pack
        self._context_budget = ctx_budget
        self._context_files = file_count
        self._context_tokens = estimate_tokens(pack)
        self._session.add_message("system", pack)
