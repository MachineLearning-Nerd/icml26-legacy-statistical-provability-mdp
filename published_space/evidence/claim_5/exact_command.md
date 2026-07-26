# Exact command and compute contract

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Pinned dependencies are in `uv.lock`. Seed-free exact rational and SMT checks
are deterministic. Expected scientific requirement: one CPU core and less than
one minute. The Hugging Face run records the container-visible CPU count and
runtime. The selected `cpu-upgrade` contract allocates 8 vCPUs; Python's
`os.cpu_count()` reported 64 host logical CPUs visible to the container, which
is recorded separately and is not called the allocation.
