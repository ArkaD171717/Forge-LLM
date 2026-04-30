# Getting started

## Install

The metapackage pulls in the core libraries:

```bash
pip install forge-infer
```

Or install individual packages if you only need one layer:

```bash
pip install qwen-think     # session management
pip install qwen3.6-mtp    # MTP tuning
pip install qwen3-repo      # repo ingestion
```

## Session layer: thinking mode control

qwen-think manages when and how Qwen3.6 "thinks" -- toggling thinking on/off, swapping sampling parameters atomically, and guarding context budget.

```python
from forge.session import ThinkingSession

session = ThinkingSession(
    model="Qwen/Qwen3.6-27B",
    backend="vllm",
    budget=200_000,
)

# Thinking mode: temp=0.6, top_p=0.95, top_k=20
response = session.chat("Refactor this module for testability", thinking=True)

# Instruct mode: temp=0.7, top_p=0.80, presence_penalty=1.5
response = session.chat("What's the return type of foo()?", thinking=False)
```

The backend normalizer handles the divergent flag formats across vLLM (`extra_body.enable_thinking`), DashScope (`extra_body.enable_thinking` at top level), and llama.cpp (server-side flag).

## Optimize layer: MTP speculative decoding

qwen3.6-mtp recommends MTP configuration based on your hardware, use case, and objective. It also detects known-broken configurations (e.g., TurboQuant + MTP produces degenerate token loops).

```python
from forge.mtp import recommend, UseCase, Objective

rec = recommend(
    use_case=UseCase.SINGLE_USER,
    objective=Objective.MINIMIZE_LATENCY,
    gpu_id="rtx-4090",
)
print(f"Enable MTP: {rec.enable}")
print(f"Expected gain: {rec.expected_gain}")
print(f"Speculative tokens: {rec.num_speculative_tokens}")
```

### Find the crossover point

MTP helps single-user latency but hurts throughput at higher batch sizes. Find where it flips:

```python
from forge.mtp import quick_crossover

for s in quick_crossover(gpu_id="rtx-3090"):
    print(f"MTP-{s.spec_tokens}: crossover at batch {s.crossover_batch_size}")
```

### Generate backend serve commands

```python
from forge.mtp import vllm_mtp_command, sglang_mtp_command

cmd = vllm_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2)
print(cmd.command)

cmd = sglang_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2)
print(cmd.command)
```

## Context layer: repo ingestion

qwen3-repo ingests a repository into Qwen3.6's context window with dependency-ordered file packing, importance ranking, and vision asset detection.

```python
from qwen3_repo import ingest_repo

context_pack, files, budget = ingest_repo(
    "https://github.com/user/repo",
    model="Qwen3-32B",
)
print(f"{len(files)} files, ~{budget.pack_budget:,} tokens")
```

Ordering matters for linear attention: Gated DeltaNet processes tokens sequentially with a fixed-size recurrent state. Putting high-dependency files late (after their dependents) means the model sees call sites before definitions. qwen3-repo orders by dependency graph to avoid this.

## Compat layer: what works and what doesn't

qwen-compat is a test matrix and upstream bug fix collection, not a library. Clone it and run the matrix:

```bash
git clone https://github.com/ArkaD171717/Qwen3.6-Compat
cd Qwen3.6-Compat
./benchmark/compat_matrix.sh --backend ollama
```

See [Compat](layers/compat.md) for the current status of known bugs and upstream PRs.
