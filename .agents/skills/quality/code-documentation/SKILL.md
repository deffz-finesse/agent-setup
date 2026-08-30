---
name: code-documentation
description: Review and improve documentation for code changes or named source files across programming languages and development harnesses. Use when creating, editing, reviewing, or auditing source code, tests, public APIs, packages, modules, configuration contracts, CLI behaviour, migrations, or repository documentation that must remain aligned with code. Prefer self-documenting code, follow the repository's established documentation system, document public contracts and non-obvious intent, and remove stale or redundant comments. Skip prose-only changes that do not describe code behaviour.
---

# Code documentation

Produce documentation that helps maintainers use, test, change, and operate code safely. Do not narrate syntax or aim for uniform comment density.

Keep all required behaviour in `SKILL.md` and `references/`. Treat harness-specific metadata as an optional adapter, never as the source of documentation rules.

## Establish the local standard

Before writing documentation, inspect the affected code and the nearest repository guidance. Look for:

- `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, developer guides, and local equivalents;
- documentation configuration, linters, generators, spelling rules, and CI checks;
- nearby public API, package, module, file, test, and symbol documentation;
- READMEs, architecture records, schemas, migration guides, testing guides, and changelogs;
- generated-file notices, licensing requirements, and canonical documentation sources.

Treat explicit local conventions as authoritative unless they would make the documentation false, insecure, or incompatible with the task. Do not introduce a second documentation system without a clear need.

Read:

- [references/documentation-surfaces.md](references/documentation-surfaces.md) when repository, API, configuration, CLI, architecture, deployment, migration, or release documentation may be affected.
- [references/language-conventions.md](references/language-conventions.md) for the languages and file formats present in the task.
- [references/test-documentation.md](references/test-documentation.md) when tests, fixtures, examples, snapshots, test helpers, or testing instructions are in scope.
- [references/examples.md](references/examples.md) when a concrete comparison would help.

## Set the scope

For a code change, inspect the task-owned branch, staged, and unstaged diffs. Include callers, tests, schemas, generated sources, and existing documentation only as needed to understand the changed contract.

Do not edit unrelated files merely because their documentation could be improved.

If no diff exists, use the paths or symbols named by the user. For a repository-wide audit, inventory the documentation systems and report the highest-risk gaps before making broad changes.

If the task is review-only, report concrete findings and locations. Do not modify files without authorization.

## Decide where information belongs

Put information in the narrowest canonical location that serves its readers:

1. Encode enforceable facts in names, types, schemas, validation, tests, or clearer structure.
2. Put user and operator behaviour in the relevant README, command reference, configuration reference, API description, migration guide, or runbook.
3. Put reusable public contracts on the exported package, module, type, function, method, property, command, or configuration key.
4. Put file-wide responsibility, boundaries, and shared invariants in a file or module overview.
5. Put local rationale and implementation invariants beside the code they constrain.
6. Put architectural decisions in an ADR, RFC, design document, or established equivalent.
7. Put demonstrated edge cases and regressions in tests while keeping supported public behaviour documented at the public interface.

Do not duplicate the same rule across several locations. Link to the canonical explanation when repetition would create competing sources of truth.

## Review workflow

1. Identify changed behaviour, public symbols, tests, configuration, errors, side effects, compatibility promises, and non-obvious logic.
2. Trace enough callers and data flow to confirm ownership, lifecycle, failure modes, and externally visible effects.
3. Improve names, types, structure, validation, or test names when that removes the need for explanatory prose without expanding the task.
4. Determine which documentation locations the change affects.
5. Use the language's native documentation form and the repository's existing markup, tags, and generator.
6. Review affected tests as executable evidence of behaviour.
7. Re-read code, tests, and documentation together.
8. Remove filler, stale claims, duplicated type information, broken links, dead examples, and accidental secrets.
9. Run relevant documentation linting, generation, doctests, example tests, link checks, spelling checks, or repository validation when available.

## File and module overviews

Add a file or module overview when maintainers need context before reading individual symbols.

A useful overview may explain:

- the file's responsibility;
- what the file deliberately does not own;
- its relationship to neighbouring modules;
- shared invariants across several symbols;
- lifecycle or resource ownership;
- concurrency or synchronization rules;
- architectural or protocol boundaries;
- why the file exists when its placement is not self-explanatory.

Do not use overview headers to repeat the filename, list visible exports, describe obvious control flow, record authorship or dates, maintain a source changelog, add decorative banners, or satisfy a uniform header policy the repository does not have.

Add legal, copyright, generated-file, or tooling headers only when required by the repository or build system.

## What merits documentation

Document information that code alone does not express clearly, especially:

- public behaviour, preconditions, postconditions, stability, and compatibility;
- error meaning, retryability, partial success, and observable side effects;
- units, ranges, sentinel values, ordering, time bases, and precision;
- ownership, resource lifetime, mutability, thread safety, locking, and cancellation;
- state-machine, parser, protocol, serialization, and migration invariants;
- security and privacy boundaries without exposing secrets or useful exploit details;
- deliberate performance trade-offs or complexity constraints;
- workarounds tied to an upstream issue, platform limitation, or version;
- business rules whose reason cannot be recovered from the expression;
- deprecation paths and replacement behaviour;
- test setup whose purpose cannot be inferred from the test;
- fixture assumptions that affect several tests.

## What to leave undocumented

Avoid comments or documentation blocks that:

- restate a name, type, signature, assertion, control flow, or the next line;
- list parameters and return types without adding semantics;
- explain standard language syntax or a familiar library call;
- preserve dead code, authorship history, or change logs inside source files;
- make promises that are not enforced, tested, or intended as supported behaviour;
- describe implementation details as stable public guarantees;
- use headings and boilerplate merely to make a file look complete;
- explain what a test does when its name and assertions already show it.

Comment density should follow risk. A short public function with subtle failure semantics may need more documentation than a long internal function with obvious data flow.

## Tests as documentation

Treat tests as executable evidence of behaviour, not as the sole public contract.

Check that:

- test names describe the condition and expected behaviour;
- regression tests explain the reason only when the test body cannot;
- unusual timing, concurrency, malformed input, tolerances, mocks, or platform setup have enough context;
- shared fixtures document important defaults, ownership, cleanup, and hidden effects;
- examples compile or execute when the repository supports it;
- tests and public documentation agree;
- accidental implementation details are not presented as compatibility promises.

Do not weaken, remove, or rewrite meaningful assertions merely to make documentation simpler.

## Keep documentation maintainable

- Update the canonical source for generated documentation, then regenerate its outputs.
- Never hand-edit generated files.
- Keep examples minimal and executable when suitable tooling exists.
- Use issue-linked TODO, FIXME, HACK, and workaround comments when the repository supports issue tracking.
- State the removal condition for temporary workarounds.
- Preserve terminology, capitalization, links, and vocabulary used by the public interface.
- Never place credentials, tokens, private endpoints, personal data, production exports, or realistic secrets in comments, fixtures, or examples.
- Do not add documentation solely to satisfy a percentage target unless the repository explicitly enforces one.
- Do not add a new documentation generator, linter, or standard unless the task includes establishing or changing the documentation system.
