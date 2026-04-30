# Cloud layer: forge-cloud

OpenAI-compatible reasoning-aware inference proxy. Points your existing OpenAI client at forge-cloud instead of directly at vLLM/Ollama, and it auto-routes thinking mode, manages context budget, tunes MTP, and blocks known-broken configs.

## How it works

1. You send a standard OpenAI chat completion request to forge-cloud
2. forge-cloud inspects the request: query complexity, model target, backend
3. The session layer (qwen-think) decides: thinking mode on/off, sampling params, context budget
4. The optimize layer (qwen3.6-mtp) checks: is MTP appropriate? Any blocked combos?
5. Request is forwarded to your backend (vLLM, SGLang, Ollama, DashScope)
6. Response comes back instrumented (thinking tokens vs response tokens, budget consumption)

## Install

```bash
pip install forge-cloud
```

## Usage

```bash
export FORGE_ADMIN_KEY=my-secret
export FORGE_BACKEND_URL=http://localhost:8000
forge-cloud  # runs on port 8741
```

Then point your OpenAI client at it:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8741/v1", api_key="your-key")
response = client.chat.completions.create(
    model="Qwen/Qwen3.6-27B",
    messages=[{"role": "user", "content": "Explain merge sort"}],
)
```

forge-cloud handles thinking mode routing, parameter swaps, and backend normalization transparently.

## What it includes

- Complexity-based routing (think vs. no-think)
- API key management and rate limiting
- SQLite-backed usage tracking
- CI/CD workflows

!!! note "Status"
    forge-cloud is built and tested locally. It is not yet deployed as a hosted service. The proxy code is open-source. A hosted version at a public endpoint is planned if there is sufficient demand from the community. See [roadmap](../roadmap.md).
