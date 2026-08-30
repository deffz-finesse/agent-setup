<!-- workflow:context -->

## Cyril agent workflows

Repository-local agent instructions and workflow skills for the Cyril tooling project. Python tooling uses `uv`; workflow source lives under `_agent-workflows/` and `.agents/`. The canonical workflow manifest is `_agent-workflows/_config/help.csv`.

## Where things are

- Local skills: `.agents/skills/`; each skill is defined by its `SKILL.md` frontmatter and body.
- Run workspaces: `_artifacts/runs/<run-slug>/`; lifecycle structure and ownership are defined in `_agent-workflows/_config/artifact-lifecycle.md`.
- Workflow renderer: `_agent-workflows/scripts/render_skill.py`.
- Workflow manifest: `_agent-workflows/_config/help.csv`.
- Run-state helper: `_agent-workflows/scripts/run_state.py`.
- Project and developer dependencies: `pyproject.toml`, `uv.lock`, and `package.json`.

## Running and verifying

- For `implement`, run the exact `uv run --no-cache "{project-root}/_agent-workflows/scripts/render_skill.py" --project-root "{project-root}" --skill "{skill-root}"` command once, then follow the generated workflow.
- Start a new initiative with `uv run _agent-workflows/scripts/run_state.py init --project-root "{project-root}" --title "<title>"`; validate it with the same helper before resuming or handing it off.
- Add one atomic, commit-sized implementation slice with `uv run _agent-workflows/scripts/run_state.py add-slice --run-dir "<run-dir>" --number <N> --title "<title>"`. A sprint or branch may contain several slices. Planning another slice does not change `active_slice`; select it explicitly with `set-active-slice`, update its canonical state with `set-slice-status`, and update lifecycle state with `set-phase`.
- Register every run artifact with `uv run _agent-workflows/scripts/run_state.py add-artifact --run-dir "<run-dir>" --path "<phase-dir>/<file>" --type <type> --status <draft|current>`. Mark `--blocking` when the artifact records a finding that must be resolved before later-phase artifacts are added; unblock it later by re-registering that same entry with `--waived --waiver-reason "<why>"` (see `_agent-workflows/_config/artifact-lifecycle.md`). Call `set-phase` at each phase transition — `validate` rejects a run whose artifacts have advanced past the recorded `phase`, and rejects any artifact registered past an unresolved, unwaived blocker.
- Read a skill's required `customize.toml`, references, templates, and scripts after that skill activates; they configure execution and do not trigger the skill.
- When an artifact contains claims about current libraries, APIs, frameworks, tools, market conditions, or external behavior, gather evidence before writing the claim. Use `context7-mcp` for current named library/framework/API documentation, `opensrc` for dependency implementation details, `gh` for repository/issue/release and primary-source GitHub evidence, `playwright-mcp` for live web-app behavior, and `deep-recon` for broader market/domain/competitive/literature research.
- Before researching or drafting any time-sensitive artifact, obtain the runtime date from the environment, not model memory, and establish an `as_of` date for the run. In this WSL environment, use `date -u +%Y-%m-%d` or an equivalent runtime-clock check. Use that date in research queries and artifact metadata. For package or tool versions, resolve the exact version available as of that date and record the version, source, publication/release date when available, and retrieval date; never call a remembered version “latest.”
- On resumed runs, capture a new retrieval date for newly verified claims while preserving the original date on unchanged evidence. Distinguish `as_of` date, source publication/release date, and retrieval date; do not silently present old evidence as current.
- Record load-bearing external evidence in the owning artifact's source/import/digest files and process log. Include the source, version or retrieval date when relevant; do not treat model memory or an unverified search result as evidence.
- Keep `_agent-workflows/_config/help.csv` aligned when adding, removing, or renaming workflow skills. It does not replace the `SKILL.md` files for persona skills or special activation rules.

## Conventions that differ from defaults

- Infer the applicable local skill from the user's intent; do not ask the user to name or invoke a skill when the request matches a skill description.
- Route requests in this order: explicit skill/persona request; explicit activity or artifact; required cross-cutting policy; then the narrowest semantic match in the skill descriptions and `help.csv`.
- Before acting, load the primary skill's `SKILL.md`, then load supporting or prerequisite skills named by it. A skill is active only after its instructions have been loaded; loading a skill does not itself execute its tools or scripts.
- Treat a direct request to build, fix, review, plan, research, explain, test, or document something as sufficient activation for the matching workflow skill. Do not ask the user to repeat the request as a skill command.
- Use these activity routes: code changes → `implement`; PRD → `prd`; product concept → `product-brief` or `prfaq`; requirements contract → `spec`; architecture → `architecture`; epics/stories → `create-epics-and-stories`; UX planning → `ux`; sprint readiness/status → `sprint-planning`; research → `deep-recon`; retrospective → `retrospective`; acceptance tests → `testarch-atdd`; test automation → `testarch-automate`; test strategy → `testarch-test-design`; test framework → `testarch-framework`; CI quality gates → `testarch-ci`; test quality → `testarch-test-review`; NFR evidence → `testarch-nfr`; traceability → `testarch-trace`.
- Use these support routes: code documentation → `code-documentation`; naming or renaming → `naming-conventions`; GitHub inspection → `gh`; dependency internals → `opensrc`; current package/API docs → `context7-mcp`; browser exploration → `playwright-mcp`; context recovery → `recall`; workflow selection → `help`; runtime/ownership explanation → `how`; rationale/history/trade-offs → `why`.
- Use persona skills only when the user requests the persona or alias: Amelia → `dev`, John → `pm`, Winston → `architect`, Murat → `tea`, Sally → `ux-designer`, Carson → `cis-brainstorming-coach`, Maya → `cis-design-thinking-coach`, Victor → `cis-innovation-strategist`, and Dr. Quinn → `cis-creative-problem-solver`.
- For creative requests, use direct activity skills (`brainstorming`, `cis-design-thinking`, `cis-innovation-strategy`, or `cis-problem-solving`) unless the user asks for one of the named personas.
- Treat skill activation and workflow tool calls as separate events: frontmatter selects a skill, while the body controls what happens afterward.
- Do not make the user invoke ordinary workflow skills. Honor exceptions declared by the skill itself: `project-context` requires invocation by name, `grilling` is explicit opt-in, and `unslop` always applies.
- Apply `commit-conventions` before any Git mutation, including staging, branching, committing, pushing, or opening a pull request.
- Resolve overlapping review requests explicitly: use `code-review` for adversarial code review; `review` for multi-lens review of a diff, document, spec, or artifact; `checkpoint-preview` for a human walkthrough; and `code-documentation` when the requested change is documentation tied to code behavior.
- Resolve planning overlaps explicitly: use `product-brief` when the concept is already chosen, `prfaq` when it should be challenged customer-first, `prd` for product requirements, `spec` for a compact implementation-independent contract, and `architecture` for deciding how an agreed requirement should be built.
- Resolve elicitation overlaps explicitly: use `advanced-elicitation` to improve an existing draft, `grilling` only for an explicit relentless interview, and ordinary workflow questioning for normal clarification.
- If multiple skills apply, choose one primary workflow and add only skills that provide a required policy, tool, or handoff. If two primary workflows would produce materially different artifacts, ask about the artifact, not which skill to invoke.
- When a run under `_artifacts/runs/<slug>/` is active, artifact-producing skills write into that run's owning phase and register the result with `run_state.py add-artifact`; there is no standalone artifact fallback. `00-discovery/` preserves raw input and decisions, `01-research/` owns sources and evidence digests, `02-plan/` holds a deliberately rough overall plan and shared constraints, and `03-slices/` holds the current sprint plus just-in-time commit-sized slice plans. Do not pre-plan every implementation detail or treat a branch/epic as one slice. `04-implementation/` remains empty until effectful product implementation has actually produced evidence.
- Repository-maintenance work on the workflow definitions is not a Cyril product artifact. Do not create a Cyril initiative run or product slice for changes limited to `.agents/`, `_agent-workflows/`, `AGENTS.md`, or their workflow tests unless the user explicitly makes that maintenance itself a tracked product initiative.
- Treat new input material that conflicts with, or materially expands, the scope already recorded in an earlier discovery artifact as a required cross-cutting policy trigger: persist the raw source verbatim under `00-discovery/` before deriving anything from it, and surface the scope delta to the user explicitly before treating the new material as authoritative.
- Automatic activation (the rule above that ordinary workflow skills are not manually invoked) still means running that skill's full activation → body → finalize sequence. Producing a same-shaped artifact without it skips the skill's own discovery rigor, memlog audit, and doc-standards passes, and does not satisfy the workflow.

## Known pitfalls

- Do not treat a skill name or a command mentioned inside a skill as an automatic tool call; load the skill first and follow its stated workflow.
- Do not assume a broad semantic trigger is exclusive. Check neighboring skills when a request could match more than one description.
- Do not let a corrupted, ambiguous, or inconsistent term surfaced during source normalization (a transcription artifact, a term that conflicts with earlier terminology) propagate into a downstream artifact verbatim; resolve it against the source or the user before it appears in generated output.

<!-- /workflow:context -->
