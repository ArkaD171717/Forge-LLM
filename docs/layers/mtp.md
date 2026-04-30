# Optimize layer: qwen3.6-mtp

[GitHub](https://github.com/ArkaD171717/Qwen3.6-MTP) | [PyPI](https://pypi.org/project/qwen3.6-mtp/)

Hardware-aware MTP (Multi-Token Prediction) speculative decoding auto-tuner for Qwen3.6. Recommends configuration, generates vLLM/SGLang serve commands, finds throughput crossover points, and detects known-broken configs.

## What it does

- **Auto-tuner**: takes your use case (single/multi-user), objective (latency/throughput), and GPU class; outputs MTP config or disables with a reason
- **Backend configs**: generates vLLM (`method: mtp`) and SGLang (`NEXTN` algorithm) serve commands
- **Crossover analysis**: finds the batch size where MTP flips from net-positive to net-negative
- **Bug detection**: blocks TurboQuant + MTP (degenerate token loops, vLLM #40831), detects prefix cache degradation

## Install

```bash
pip install qwen3.6-mtp
```

## Usage

### Recommendation

```python
from forge.mtp import recommend, UseCase, Objective

rec = recommend(
    use_case=UseCase.SINGLE_USER,
    objective=Objective.MINIMIZE_LATENCY,
    gpu_id="rtx-4090",
)
print(f"Enable: {rec.enable}")
print(f"Expected gain: {rec.expected_gain}")
print(f"Tokens: {rec.num_speculative_tokens}")
```

### Crossover analysis

```python
from forge.mtp import quick_crossover

for s in quick_crossover(gpu_id="rtx-3090"):
    print(f"MTP-{s.spec_tokens}: crossover at batch {s.crossover_batch_size}")
```

### Serve commands

```python
from forge.mtp import vllm_mtp_command, sglang_mtp_command

print(vllm_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2).command)
print(sglang_mtp_command(model="Qwen/Qwen3.6-27B", num_speculative_tokens=2).command)
```

## Key findings

These are baked into the tuner's recommendations:

- **+27.5% faster decode TPOT** at k=1 on RTX 3090 (with `--no-enable-prefix-caching`)
- MTP is strictly a **latency win for single-user/low-concurrency**, throughput loss for high-concurrency
- **Crossover point**: batch size 4-8 on consumer GPUs
- MTP is algorithmically **lossless** -- does not constrain sampling parameters
- An earlier -12% throughput finding was a flag confound (prefix-cache interaction, not MTP problem)

## Known bugs tracked

- **vLLM prefix cache + MTP** (#38182): drops last matched block when MTP is enabled, hit rate falls from ~92% to ~71%
- **TurboQuant + any spec-decode** (#40831): degenerate token loops across dense and hybrid architectures. The tuner detects and blocks this combination.
