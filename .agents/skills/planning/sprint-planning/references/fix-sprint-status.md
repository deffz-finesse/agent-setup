# Fix Sprint Status

1. Run `sprint_plan.py validate` and show the problems.
2. Read existing `03-slices/*/slice.yaml` files and git evidence. Do not infer
   that a planned slice was implemented merely because its plan exists.
3. Propose a corrected sprint goal and ordered list containing only the current
   short horizon. Move distant candidates to `03-slices/backlog.md`.
4. Ask the user to confirm additions, removals, reordering, and any status
   correction. Headless mode blocks.
5. Rewrite `sprint-status.yaml`, update individual `slice.yaml` files only when
   evidence supports the status, then validate again.

Never rebuild a project-wide story monolith from the rough roadmap.
