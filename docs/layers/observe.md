# Observe layer: forge-observe

[GitHub](https://github.com/ArkaD171717/Forge-Infer)

OpenTelemetry instrumentation for the reasoning layer. Every observability platform in 2026 captures tool call spans and agent graph nodes, but the actual thinking block content, budget consumption, and preserve_thinking utilization are invisible to all of them. forge-observe instruments that layer.

## What it instruments

- **Thinking budget burn rate**: how fast the 128K+ budget is being consumed
- **Think vs. response token split**: what fraction of output tokens are thinking vs. user-facing
- **preserve_thinking utilization**: is the model reusing prior thinking across turns, or regenerating
- **Mode switch events**: when the router flips between thinking and instruct mode, and why
- **Backend flag normalization**: which backend path was used (vLLM nested, DashScope top-level, llama.cpp server-side)
- **Sampling param swaps**: logs when the atomic think/instruct parameter swap fires

## Install

```bash
pip install forge-observe
# with OTLP exporter:
pip install forge-observe[otlp]
```

## Usage

### Auto-instrumentation

```python
from forge_observe import instrument

instrument()  # patches qwen-think sessions automatically

from qwen_think import ThinkingSession
session = ThinkingSession(client=your_client)
response = session.chat("Implement a binary search tree")
# Spans and metrics are emitted to your configured OTel backend
```

### Manual tracer

```python
from forge_observe import ForgeTracer

tracer = ForgeTracer()
with tracer.thinking_span("complex-query") as span:
    span.set_attribute("forge.thinking.budget_remaining", 180_000)
    span.set_attribute("forge.thinking.mode", "thinking")
    # ... your inference call ...
```

## OTel integration

Standard OTel SDK. Emits spans and metrics that can be collected by any OTel-compatible backend. If you already have observability infra, forge-observe plugs into it:

- Jaeger
- Grafana Tempo
- Datadog

Example configs for each backend are included in the repo under `examples/`.

!!! note "Status"
    forge-observe is built and functional. It is not yet published on PyPI. See [roadmap](../roadmap.md) for details.
