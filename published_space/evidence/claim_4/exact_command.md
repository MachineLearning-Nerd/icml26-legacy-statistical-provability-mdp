# Fixed command and environment

Every node runs exactly:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Python is pinned to 3.12 by `.python-version`; all dependencies are locked by
the repository `uv.lock`. No run-time environment variable changes theorem
behavior.
