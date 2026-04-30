# Compat layer: qwen-compat

[GitHub](https://github.com/ArkaD171717/Qwen3.6-Compat)

Compatibility test matrix and upstream bug fixes for running Qwen3.6 on consumer-grade local inference. This is not a library -- it's a collection of test scripts, upstream PRs, and a pass/fail grid across backends.

## Bug tracker

| Bug | Backend | Status | Notes |
|-----|---------|--------|-------|
| mmproj clip runner missing qwen35moe | Ollama | PR submitted ([#15899](https://github.com/ollama/ollama/pull/15899)) | Community GGUFs with separate mmproj files fail with "unknown model architecture: 'qwen35moe'" |
| NVFP4 corrupted K-projection weights | Ollama | PR submitted ([#15902](https://github.com/ollama/ollama/pull/15902)) | in_proj_qkv and in_proj_z need BF16 exemption during NVFP4 quantization |
| Format ignored with think=false | Ollama | PR submitted ([#15901](https://github.com/ollama/ollama/pull/15901)) | Structured output format not applied when thinking is disabled |
| preserve_thinking on 27B GGUF | llama.cpp | Resolved upstream | Works on HEAD (build b8985). No PR needed. |
| IQ4 Metal throughput regression | llama.cpp | Resolved upstream | llama.cpp #21655 closed |
| TurboQuant + speculative decoding | vLLM | Open (#40831) | Degenerate token loops. Not an Ollama/llama.cpp issue. Detected and blocked by qwen3.6-mtp tuner. |

## Test matrix

Clone the repo and run the compatibility matrix:

```bash
git clone https://github.com/ArkaD171717/Qwen3.6-Compat
cd Qwen3.6-Compat
./benchmark/compat_matrix.sh --backend ollama
./benchmark/compat_matrix.sh --backend llamacpp
```

The matrix tests text generation, preserve_thinking, and quantization throughput across vLLM, SGLang, Ollama, and llama.cpp backends.
