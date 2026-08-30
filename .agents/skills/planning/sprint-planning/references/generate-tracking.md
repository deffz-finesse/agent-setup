# Plan the Next Sprint

1. Review the rough plan with the user and select one immediate horizon.
2. Propose one to five ordered slices. For each, state:
   - one atomic outcome;
   - why it is independently reviewable;
   - dependencies on earlier slices;
   - concise acceptance checks; and
   - the expected single-commit boundary.
3. Split any proposal containing independently useful/revertible parts. Do not
   use a branch name, epic, or whole feature as the slice boundary.
4. Get user approval for the short sequence. Headless mode blocks instead of
   inferring priority.
5. Create each approved slice with:

   ```text
   uv run _agent-workflows/scripts/run_state.py add-slice \
     --run-dir "{run_dir}" --number <N> --title "<atomic outcome>"
   ```

6. Fill each slice's `plan.md` and `acceptance.md` just enough for that commit.
   Keep wider context as links; do not copy the whole project plan into each
   slice.
7. Write `{run_dir}/03-slices/sprint-status.yaml` from
   `sprint-status-template.yaml`. It contains the sprint goal and `slice_order`
   only. Each referenced directory's `slice.yaml` remains the status authority.
8. Move unselected ideas to `{run_dir}/03-slices/backlog.md` as brief candidates,
   not implementation records.
9. Run `sprint_plan.py validate`, register the status file, backlog when present,
   and all slice files, then set the run phase to `slice-planning`.
