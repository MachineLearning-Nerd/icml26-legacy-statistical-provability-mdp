# Fixed command and environment

Every node runs exactly:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Python is pinned to 3.12 and all executable dependencies to `uv.lock`. The
topological derivation has no numerical tolerance or stochastic seed.
