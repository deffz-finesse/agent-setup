# Artifact lifecycle

Each initiative gets one stable run workspace under `_artifacts/runs/<run-slug>/`.
The run is the user-facing unit of work; individual skills are workers for one
phase of that run. `_artifacts/runs/` is the only artifact root. The root is
configured by `core.runs_root` in `_agent-workflows/_config/config.toml`; consumers
must resolve that key rather than reconstructing a legacy path.

```text
<run-slug>/
├── README.md                         # human-facing status and links
├── run.yaml                          # canonical run state
├── 00-discovery/                     # conversation and decisions
├── 01-research/                      # research plan, sources, imports, digests
├── 02-plan/                          # rough overall plan and shared constraints
├── 03-slices/                        # just-in-time sprint and commit-sized slice plans
│   ├── sprint-status.yaml            # ordered coordination view; slice.yaml owns status
│   ├── backlog.md                    # candidate work not yet promoted to a slice
│   └── 001-<slice>/
│       ├── slice.yaml                # canonical slice state
│       ├── plan.md
│       └── acceptance.md
├── 04-implementation/               # evidence from implementation that actually ran
├── 05-testing/                       # test plans, reports, and evidence
├── 06-review/                        # review report and findings
├── 07-release/                       # release checklist and PR summary
└── 08-retrospective/                 # lessons and follow-through
```

`run.yaml` is the index. Its `phase`, `status`, `active_slice`, `as_of`, and
`artifacts` fields tell a new session where to continue. `slice.yaml` owns the
status of one atomic implementation slice. A slice is normally one coherent
commit: a branch or sprint may contain several slices, but a slice must not be
used as a synonym for either. `.memlog.md` remains append-only
process memory inside the phase that owns it; it does not replace `run.yaml`.
Every durable file written below the run is registered with `run_state.py
add-artifact` using a path relative to the run root. A current artifact is
complete phase evidence; a draft is resumable work and does not advance the
recorded phase.

The transition order is discovery → research → overall-plan → slice-planning →
implementation → testing → review → release → retrospective → complete. Review
may return to implementation or slice-planning, and research may return to
discovery when the question changes.

## Blocking findings and phase gates

An artifact entry may set `blocking: true` when it records a finding that must
be resolved before work moves to a later phase — for example, an unresolved
conflict between newly supplied material and an earlier discovery artifact, or
a canonical source that still needs to be persisted and normalized. While an
unresolved blocker exists, `run_state.py validate` and `add-artifact` refuse to
register or keep any artifact in a later phase directory than the blocker.
Resolve the finding and drop `blocking`, or explicitly accept the risk by
re-registering the _blocking_ entry itself (`add-artifact` upserts by path)
with `waived: true` and a `waiver_reason` — waiving is a deliberate, visible
call, not a default path around the gate.

`run_state.py validate` also rejects a run whose registered artifacts reach a
later phase directory than `run.yaml`'s recorded `phase`. Call `set-phase` at
each transition so the manifest and the artifacts on disk stay in agreement —
do not let a directory fill up with later-phase output while `phase` still
names an earlier one.

### Phase ownership

| Phase | Durable output owned by the phase |
| --- | --- |
| `00-discovery/` | discovery notes, creative/CIS sessions, brainstorming, and their memlogs |
| `01-research/` | research plans, source imports, digests, and evidence memlogs |
| `02-plan/` | a deliberately rough overall plan, product direction, capability horizons, and shared architecture/UX constraints; no exhaustive implementation story inventory |
| `03-slices/` | current sprint coordination in `sprint-status.yaml`, candidate work in `backlog.md`, and just-in-time slice folders |
| `03-slices/<NNN-slug>/` | one commit-sized goal's `slice.yaml`, focused context, plan, and acceptance criteria |
| `04-implementation/` | implementation logs, changed-file/commit records, and other evidence emitted only after effectful work begins |
| `05-testing/` | ATDD, test design, framework/CI records, automation, NFR, and traceability evidence |
| `06-review/` | review and code-review reports, including each scoped test review |
| `07-release/` | release checklists, summaries, and handoff records |
| `08-retrospective/` | dated retrospective reports and follow-through evidence |

The planning and delivery skills require an active run. The Create flow of
`product-brief` (or `prd`) is the initiative-starting flow: when no active run
exists it offers to initialize a named run with `run_state.py init`; ambiguous
headless input stops without creating one. Other skills select exactly one
active run (multiple active runs require explicit selection) and bind to the
phase above. They never write to a standalone artifact root.

For a repeated workflow, include the stable target slug (story, epic, topic,
date, or another required identity) in the filename or child folder. A missing
target identity is an error before writing. Never silently overwrite an
existing quality artifact; choose a new scoped path or update the explicitly
selected artifact.

The migration is complete: `planning-artifacts`, `implementation-artifacts`,
`specs`, and `test-artifacts` are retired legacy roots. Existing content is
moved into the owning run phase and indexed exactly once; new integrations
must register into `run.yaml` rather than creating another top-level
convention.

## Progressive planning rule

Planning proceeds from coarse to specific. The user and agents first agree a
rough overall project plan in `02-plan/`: outcomes, major capability horizons,
dependencies, risks, and architecture invariants. They intentionally do not
write every story or lock implementation details for the entire initiative.

Sprint planning then selects only the next useful horizon and decomposes it
into a short ordered set of coordinated slices under `03-slices/`. Each slice
has one atomic goal and should be implementable as one coherent commit. If two
parts could be reviewed, reverted, or shipped independently, they are separate
slices. Later slices are refined only after earlier implementation evidence is
available; the rough plan may be revised as the project teaches us more.

`04-implementation/` is an evidence phase, not a planning or backlog folder.
Creating a sprint rollup, compiling context, or deferring a candidate does not
prove implementation occurred and must not populate it. The directory may be
empty while the run is in discovery, research, overall planning, or slice
planning.
