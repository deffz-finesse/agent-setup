# Readiness Gate

Judge only whether the next small implementation step can be planned without
inventing load-bearing decisions. Scan the rough plan and shared constraints in
`{run_dir}/02-plan/`, relevant research in `{run_dir}/01-research/`, the current
backlog, and any existing slices.

Ask: **Can we define the next one to five atomic commits, while deliberately
leaving later work rough?**

- **PASS** — the next horizon, dependencies, and acceptance boundary are known.
- **CONCERNS** — planning can proceed after the user accepts named local risks.
- **FAIL** — the next slice requires unresolved product, research, architecture,
  or sequencing decisions.

Do not fail because distant epics lack detailed stories. Do fail when the next
candidate is branch-sized, mixes independently reviewable goals, or depends on
unverified decisions. For a full planning request, continue to
`generate-tracking.md` after PASS or accepted CONCERNS.
