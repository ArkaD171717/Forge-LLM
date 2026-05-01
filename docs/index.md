# Forge

**Framework for Orchestrating Reasoning in Generative Engines**

!!! warning "Early alpha -- everything here is a work in progress"
    This entire project is in very early alpha. The libraries are functional but APIs will change, docs are incomplete, and nothing is production-ready. If you're here, you're early. Expect rough edges.

Inference control plane for reasoning-aware open-source models.

The three dominant self-hosting tools -- vLLM, SGLang, Ollama -- are pipes. They move tokens between your application and the inference engine, but none of them have a layer that understands thinking modes, hybrid KV memory profiles, or speculative decoding tradeoffs. Forge builds that layer.

Qwen3.6 is the starting point because it makes these problems explicit (thinking toggling, MTP, linear attention context budgets), but the same patterns show up in Mistral Small 4, GLM-5.1, and DeepSeek V4.

## Architecture

<figure markdown="span">
  ![Forge architecture](assets/architecture.svg){ width="100%" }
</figure>

Each layer has a clean contract with the one below it. ForgeEngine is the integration point that chains session + MTP + context into one configure-once object. The product layers (cloud proxy, dashboard, observe) sit on top. Apps (forge-studio, Open WebUI plugins) are the user-facing front doors.

## Install

```bash
pip install forge-infer
```

This pulls in [qwen-think](https://github.com/ArkaD171717/Qwen3-Think), [qwen3.6-mtp](https://github.com/ArkaD171717/Qwen3.6-MTP), and [qwen3-repo](https://github.com/ArkaD171717/Qwen3-Repo) as dependencies.

Optional extras for the product layers:

```bash
pip install forge-infer[observe]     # + forge-observe (OTel instrumentation)
pip install forge-infer[cloud]       # + forge-infer-cloud (proxy)
pip install forge-infer[dashboard]   # + forge-dashboard (observability UI)
pip install forge-infer[openai]      # + openai SDK (for ForgeEngine)
pip install forge-infer[all]         # everything
```

Individual packages are also installable standalone:

```bash
pip install qwen-think        # session management
pip install qwen3.6-mtp       # MTP speculative decoding tuner
pip install qwen3-repo        # repo-to-context ingestion
```

## Quick start

### ForgeEngine (recommended)

The integration layer that chains session + MTP + context into one object:

```python
from forge import ForgeEngine

engine = ForgeEngine(
    model="Qwen3.6-27B",
    base_url="http://localhost:8000/v1",
    gpu_id="rtx-4090",
)
engine.ingest_local("/path/to/project")
response = engine.chat("Why is the auth middleware rejecting valid tokens?")
print(engine.status())
```

### Individual layers

```python
from forge.session import ThinkingSession

session = ThinkingSession(model="Qwen/Qwen3.6-27B")
response = session.chat("Explain merge sort", thinking=True)
```

```python
from forge.mtp import recommend, UseCase, Objective

rec = recommend(
    use_case=UseCase.SINGLE_USER,
    objective=Objective.MINIMIZE_LATENCY,
    gpu_id="rtx-4090",
)
print(rec.enable, rec.expected_gain)
```

See [Getting started](getting-started.md) for more examples and the full layer-by-layer walkthrough.

## The suite

### Core libraries (Phase 1)

| Package | PyPI | What it does |
|---------|------|-------------|
| [forge-infer](https://github.com/ArkaD171717/FORGE-Infer) | `pip install forge-infer` | Metapackage + ForgeEngine integration layer |
| [qwen-think](https://github.com/ArkaD171717/Qwen3-Think) | `pip install qwen-think` | Thinking-mode session control, backend normalization, context budget |
| [qwen3.6-mtp](https://github.com/ArkaD171717/Qwen3.6-MTP) | `pip install qwen3.6-mtp` | MTP speculative decoding tuner, crossover analysis, config generation |
| [qwen3-repo](https://github.com/ArkaD171717/Qwen3-Repo) | `pip install qwen3-repo` | Dependency-ordered repo ingestion for linear attention models |
| [qwen-compat](https://github.com/ArkaD171717/Qwen3.6-Compat) | -- | Compatibility test matrix and upstream bug fixes |

### Product layers (Phase 2)

| Package | PyPI | What it does |
|---------|------|-------------|
| [forge-observe](https://github.com/ArkaD171717/FORGE-Observe) | `pip install forge-observe` | Reasoning-aware OTel instrumentation |
| [forge-cloud](https://github.com/ArkaD171717/FORGE-Cloud) | `pip install forge-infer-cloud` | OpenAI-compatible reasoning-aware inference proxy |
| [forge-dashboard](https://github.com/ArkaD171717/FORGE-Dashboard) | `pip install forge-dashboard` | Observability backend + web UI |
| [forge-studio](https://github.com/ArkaD171717/FORGE-studio) | -- | Power-user web app (FastAPI + React) |
| [Open WebUI plugins](https://github.com/ArkaD171717/FORGE-OpenWebUI) | -- | Auto-route, budget tracker, repo ingest, OTel enrichment for Open WebUI |

## License

Apache 2.0
