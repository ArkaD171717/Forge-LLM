# forge-infer

Metapackage bundling qwen-think and qwen3.6-mtp under a shared namespace.

`pip install forge-infer` pulls in [qwen-think](https://github.com/ArkaD171717/qwen3-Think) and [qwen3.6-mtp](https://github.com/ArkaD171717/Qwen3.6-MTP) as dependencies and re-exports their key APIs under a single `forge` namespace. This is packaging and narrative, not new code.

## Why this exists

Two focused packages -- thinking-mode session control and MTP speculative decoding -- that belong together. `forge-infer` gives them a shared identity so you can recommend, install, and document them as a unit instead of scattering links across READMEs.

## Install

```bash
pip install forge-infer
```

This installs both `qwen-think` and `qwen3.6-mtp` automatically.

## Quick start

### Thinking sessions (qwen-think)

Control when and how Qwen3.6 "thinks" -- budget tokens, toggle thinking on/off mid-conversation, route by complexity.

```python
from forge.session import ThinkingSession

session = ThinkingSession(model="Qwen/Qwen3.6-27B")
response = session.chat("Explain merge sort", thinking=True)
print(response)
```

### MTP speculative decoding (qwen3.6-mtp)

Tune multi-token prediction for throughput, find crossover points, generate backend configs.

```python
from forge.mtp import recommend, quick_crossover, vllm_mtp_command, sglang_mtp_command
from forge.mtp import UseCase, Objective

# Get a recommendation for your hardware
rec = recommend(use_case=UseCase.SINGLE_USER, objective=Objective.MINIMIZE_LATENCY, gpu_id="rtx-4090")
print(rec.enable, rec.expected_gain)

# Find where MTP flips from positive to negative
for s in quick_crossover(gpu_id="rtx-3090"):
    print(f"MTP-{s.spec_tokens}: crossover at batch {s.crossover_batch_size}")

# Generate serve commands
print(vllm_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2).command)
print(sglang_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2).command)
```

## Architecture

How the packages relate:

```
+---------------------------------------------+
|              forge (metapackage)             |
+------------------+--------------------------+
|   forge.session  |       forge.mtp          |
|  (qwen-think)    |   (qwen3.6-mtp)         |
|                  |                          |
|  Thinking-mode   |  MTP speculative decode  |
|  session control |  tuning & backend config |
+------------------+--------------------------+
|              Qwen3.6 model family           |
+---------------------------------------------+
```

- **forge.session** -- Re-exports ThinkingSession from qwen-think.
- **forge.mtp** -- Re-exports recommend, quick_crossover, vllm_mtp_command, sglang_mtp_command, UseCase, Objective from qwen3.6-mtp.

## Individual packages

| Package | What it does |
|---------|-------------|
| [qwen-think](https://github.com/ArkaD171717/qwen3-Think) | Thinking-mode session management |
| [qwen3.6-mtp](https://github.com/ArkaD171717/Qwen3.6-MTP) | MTP speculative decoding tuner |

## What this package does NOT do

- No new functionality -- strictly re-exports from the underlying packages
- No CLI -- the libraries are Python-first
- No model generalization -- wraps Qwen3.6-specific versions as-is

## License

Apache 2.0
