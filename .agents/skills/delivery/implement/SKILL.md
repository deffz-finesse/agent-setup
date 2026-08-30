---
name: implement
description: 'Implements any user intent, requirement, story, bug fix or change request by producing clean working code artifacts that follow the project''s existing architecture, patterns and conventions. Use when the user wants to build, fix, tweak, refactor, add or modify any code, component or feature.'
---

Run the following command exactly once without changing the current working directory. Replace `{project-root}` with the absolute path to the project root and `{skill-root}` with the absolute path to this skill's directory:

```bash
uv run --no-cache "{project-root}/_agent-workflows/scripts/render_skill.py" --project-root "{project-root}" --skill "{skill-root}"
```

- On success, read and follow the one absolute `workflow.md` instruction printed to stdout.
- On failure (including `uv` being unavailable), report the command output and HALT. Do not run any workflow source directly.

The implementation workflow must use `context7-mcp` for current documentation when a named external library, framework, SDK, or API affects the implementation; use `opensrc` when dependency internals are needed; use `gh` for primary repository/release evidence; and use `playwright-mcp` for live browser behavior or selector verification. Keep the resulting version/source evidence in the implementation spec or its referenced context files.

Implementation always runs inside one selected initiative from `core.runs_root`.
Resolve the run before routing, require explicit selection when several are active,
and bind `active_slice` from `run.yaml` to
`<run-dir>/03-slices/<active_slice>/`. Slice plans and acceptance remain there;
focused planning context stays inside that slice, sprint coordination and candidate
work stay at `<run-dir>/03-slices/`, and `<run-dir>/04-implementation/` receives
only evidence created after effectful implementation begins. A missing run or
missing `active_slice` blocks before writing. Before implementation, verify that
the active slice has one atomic, commit-sized goal expected to produce one coherent commit; a
branch or sprint may contain multiple slices. If independently reviewable work is
combined, return to slice planning and split it. Register every durable
implementation record with `run_state.py add-artifact`. There is no standalone
implementation artifact fallback.

The shared review inputs are mirrored in `quality/code-review/`: keep
`references/deletion-check.md`, `review-prompts/edge-case-hunter.md`, and
`review-prompts/verification-gap.md` byte-identical across the two skill roots.
The lifecycle contract tests pin this mirror invariant because rendered
snapshots cannot safely reference files outside their skill root.

Before selecting or upgrading a dependency, capture the runtime date and verify the exact version and support information against current sources. Record the version, source, and retrieval date in `{spec_file}` or its referenced context; never infer the latest version from model memory.
