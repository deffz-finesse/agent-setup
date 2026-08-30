# Sprint Status

Run:

```text
uv run {skill-root}/scripts/sprint_plan.py status \
  --status-file {run_dir}/03-slices/sprint-status.yaml --date "{date}"
```

Report the sprint goal, ordered slices, statuses read from each `slice.yaml`,
blocked dependencies, and the next recommended slice. An empty sprint is valid
while rough planning is still underway. Never infer implementation from the
presence of a plan file or from content under `02-plan/`.
