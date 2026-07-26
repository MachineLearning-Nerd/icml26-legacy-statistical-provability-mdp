# Fixed command and environment

Every node runs exactly:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Python is pinned to 3.12 and dependencies to `uv.lock`. The proof certificate
uses exact rational arithmetic; Z3 is independently locked by the same file.
