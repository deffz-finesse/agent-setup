# Sync Slice Status

Shared sub-step for updating the canonical `slice.yaml` during build. Called
with `target_status`.

## Preconditions

Skip only when `slice_id` or `run_dir` is unset. A missing slice file is a
blocking workflow error, not a reason to infer state elsewhere.

## Instructions

1. Read `{run_dir}/03-slices/{slice_id}/slice.yaml` and confirm its `slice_id`
   matches the directory.
2. Never regress status. The forward order is `planned` → `in-progress` →
   `testing` → `in-review` → `done`; `blocked` is explicit and may be entered
   from any incomplete state.
3. If `target_status` is later than the current state, run:

   ```text
   uv run _agent-workflows/scripts/run_state.py set-slice-status \
     --run-dir "{run_dir}" --slice-id "{slice_id}" --status "{target_status}"
   ```

4. Do not rewrite `sprint-status.yaml`; it owns ordering only and derives live
   state from each `slice.yaml`.
