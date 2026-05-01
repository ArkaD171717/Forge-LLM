# Status and roadmap

!!! warning "Early alpha"
    Everything listed here is a work in progress. "Shipped" means the code exists on PyPI and you can install it, not that it's stable or production-ready. APIs will change. This page will be updated as things solidify.

## What's shipped

### Core libraries (Phase 1)

| Package | Version | PyPI | Status |
|---------|---------|------|--------|
| qwen-think | v0.1.2 | `pip install qwen-think` | Shipped |
| qwen3.6-mtp | v0.1.1 | `pip install qwen3.6-mtp` | Shipped |
| qwen3-repo | v0.1.0 | `pip install qwen3-repo` | Shipped |
| forge-infer | v0.3.0 | `pip install forge-infer` | Shipped (includes ForgeEngine) |
| qwen-compat | -- | [GitHub](https://github.com/ArkaD171717/Qwen3.6-Compat) | Test matrix + upstream PRs |

### Product layers (Phase 2)

| Package | Version | PyPI | Status |
|---------|---------|------|--------|
| forge-observe | v0.1.1 | `pip install forge-observe` | Shipped |
| forge-infer-cloud | v0.1.2 | `pip install forge-infer-cloud` | Shipped |
| forge-dashboard | v0.1.1 | `pip install forge-dashboard` | Shipped |
| forge-studio | v0.1.0 | [GitHub](https://github.com/ArkaD171717/FORGE-studio) | Shipped (FastAPI + React) |
| Open WebUI plugins | -- | [GitHub](https://github.com/ArkaD171717/FORGE-OpenWebUI) | Shipped (4 plugins) |

### Upstream contributions

| PR | Repo | Status |
|----|------|--------|
| [#15899](https://github.com/ollama/ollama/pull/15899) | ollama/ollama | Open -- qwen35moe architecture support |
| [#15901](https://github.com/ollama/ollama/pull/15901) | ollama/ollama | Open -- format constraint for all thinking parsers |
| [#15902](https://github.com/ollama/ollama/pull/15902) | ollama/ollama | Open -- NVFP4 BF16 exemption for linear_attn |

## What's planned

**Multi-model support.** The session and routing layers are designed around Qwen3.6 today. Mistral Small 4 (configurable reasoning effort), GLM-5.1, and DeepSeek V4 (dual thinking/non-thinking mode) have the same patterns. Adding support means writing backend normalizers for each model's flag format -- the router and budget manager are already model-agnostic in structure.

**Domain-specific agents (Phase 3).** Medical coding, legal research, deep research -- same Forge infra stack with domain-tuned routing policies. Not fine-tuning models; tuning the control plane. These only make sense to build once the core tools have real users asking for them.

**Hosted deployment.** forge-cloud and forge-dashboard are both designed for self-hosting today. Managed hosting is planned if there's demand.

## How development is prioritized

New features and modules ship when there's demonstrated demand -- GitHub issues, community requests, or usage patterns that justify the work. If you're using any of these packages and have a use case that's not covered, open an issue on the relevant repo.
