# Validate Sprint Status

Run:

```text
uv run {skill-root}/scripts/sprint_plan.py validate \
  --status-file {run_dir}/03-slices/sprint-status.yaml
```

Report `valid` and each precise problem. Validation checks that every ordered
slice exists, has a valid `slice.yaml`, appears once, and respects dependencies.
It does not require every future project outcome to have a slice.
