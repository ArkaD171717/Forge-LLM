# Context layer: qwen3-repo

[GitHub](https://github.com/ArkaD171717/Qwen3-Repo) | [PyPI](https://pypi.org/project/qwen3-repo/)

Ingests a GitHub repository into Qwen3.6's context window with dependency graph ordering, importance ranking, multimodal asset detection, and benchmark parity against Qwen's NL2Repo numbers.

## Why ordering matters for linear attention

Gated DeltaNet processes tokens sequentially with a fixed-size recurrent state. Putting high-dependency files late in context (after their dependents) means the model sees call sites before definitions. Nobody has published an ordering strategy for Qwen3.6's hybrid attention architecture. qwen3-repo orders files by dependency graph so definitions come before their callers.

## Install

```bash
pip install qwen3-repo
```

## Usage

```python
from qwen3_repo import ingest_repo

context_pack, files, budget = ingest_repo(
    "https://github.com/user/repo",
    model="Qwen3-32B",
)
print(f"{len(files)} files, ~{budget.pack_budget:,} tokens")
```

## What it does

- **Dependency graph ingestion**: git clone, parse imports, topological sort
- **Importance ranking**: recently changed files, import count, test coverage
- **Vision asset detection**: scans for images/mockups, sets `--language-model-only` accordingly
- **Agentic scaffold**: OpenAI-compatible loop with bash + file-edit tools
- **Eval runners**: NL2Repo and SWE-bench Verified reproducers against Qwen's published numbers

## Context on benchmarks

Qwen3.6's NL2Repo evaluations were run via Claude Code with `temp=1.0, top_p=0.95, max_turns=900`. Both the 27B and 35B-A3B model cards still note: "NL2Repo: others are evaluated via Claude Code." No neutral third-party scaffold exists for running these evals independently. qwen3-repo is that scaffold.
