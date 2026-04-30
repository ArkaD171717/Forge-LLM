# Session layer: qwen-think

[GitHub](https://github.com/ArkaD171717/qwen3-Think) | [PyPI](https://pypi.org/project/qwen-think/)

Manages Qwen3.6's thinking state across sessions, backends, and frameworks. Normalizes the three different invocation patterns, routes requests to the right thinking mode with atomic sampling parameter swaps, and budgets context so it doesn't blow past 128K.

## What it does

- **ThinkingSession** with lifecycle and budget tracking
- **Dynamic router**: complexity classifier that picks think vs. no-think mode per request
- **Backend normalizers** for vLLM, DashScope, and llama.cpp (each has a different flag format)
- **128K context budget guard**: prevents context exhaustion from unbounded thinking
- **Atomic sampling param swap**: thinking mode uses temp=0.6/top_p=0.95/top_k=20; instruct mode uses temp=0.7/top_p=0.80/top_k=20/presence_penalty=1.5

## Install

```bash
pip install qwen-think
# or with OpenAI client support:
pip install qwen-think[openai]
```

## Usage

```python
from qwen_think import ThinkingSession

session = ThinkingSession(
    model="Qwen/Qwen3.6-27B",
    backend="vllm",
    budget=200_000,
)

# Thinking mode
response = session.chat("Refactor this module for testability", thinking=True)

# Instruct mode
response = session.chat("What's the return type of foo()?", thinking=False)

# Let the router decide
response = session.chat("Explain merge sort", preserve=True)
```

## Backend normalization

The same `enable_thinking: false` flag is passed differently depending on the backend:

| Backend | Where the flag goes |
|---------|-------------------|
| vLLM | `extra_body: { enable_thinking: false }` (nested) |
| DashScope | `extra_body: { enable_thinking: false }` (top-level) |
| llama.cpp | Server-side flag, not in the request body |

qwen-think handles this so your application code doesn't change when you switch backends.

## Known upstream bugs this works around

- **vLLM semantic-router #858**: `use_reasoning: false` removes the field instead of setting `enable_thinking: false`. Qwen3.6 thinks by default, so removing the field has no effect.
- **Ray Serve LLM v2.46**: `enable_thinking: false` in HTTP body does not propagate to the model.
- **Qwen3.6 removed prompt-prefix toggling**: The `/think` and `/no_think` prompt prefixes from Qwen3 don't work on Qwen3.6. Any framework relying on prompt-level toggling is broken.
