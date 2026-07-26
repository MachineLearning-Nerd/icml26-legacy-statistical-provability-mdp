# Fixed command and environment

Every node runs exactly:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Python 3.12 and every executable dependency are locked by repository files.
The proof and control use exact symbolic logic without numerical tolerances.
