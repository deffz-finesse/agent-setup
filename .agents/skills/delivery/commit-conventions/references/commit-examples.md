# Commit examples

Worked examples for each commit type in `commit-conventions`. Read the
category matching the commit being composed.

## Feature

```text
feat(agents): add structured GitHub CLI guidance

ADDED:
- .agents/skills/gh/SKILL.md
- .agents/skills/gh/references/gh-cli-reference.md

Agents were parsing column-formatted output and guessing pagination. Document
structured output, explicit limits, and repository targeting.
```

## Bug fix

```text
fix(tooling): resolve Node types for configuration tests

ADDED:
- tooling/tsconfig.json

EDITED:
- tooling/config.test.ts
- package.json

The editor inferred a project without Node types. Give the tooling its own
explicit TypeScript configuration.
```

## Documentation

```text
docs(contributing): clarify branch naming

EDITED:
- AGENTS.md
- docs/contributing/git-workflow.md

Keep the concise contract and detailed examples aligned on issue-optional
branch names.
```

## Tooling

```text
chore(hooks): tighten commit subject validation

EDITED:
- lefthook.yml

Align local commit checks with the repository's documented subject policy.
```

## Refactor

```text
refactor(tooling): simplify configuration report collection

EDITED:
- tooling/report.ts
- tooling/report.test.ts

Replace method wrappers with one shared collection path so callers use the
same mutation behavior.
```

## Test

```text
test(tooling): cover nested frontmatter mappings

EDITED:
- tooling/config.test.ts

Assert nested mappings do not leak into scalar configuration fields.
```

## Security

```text
security: redact token-bearing URLs from diagnostics

EDITED:
- tooling/diagnostics.ts
- tooling/diagnostics.test.ts

Strip credentials before writing remote URLs to messages or fixtures.
```

## Folder folding

```text
feat(config): add local environment templates

ADDED:
- env/**

EDITED:
- .gitignore
- README.md

Add example environment files without committing credentials. Five or more
new files under `env/` are folded to one entry.
```

Mixed change kinds in the same directory remain separate:

```text
fix(web): refresh health route assets

ADDED:
- apps/web/public/health/**

EDITED:
- apps/web/public/health/favicon.svg
- apps/web/src/routes/health.tsx

DELETED:
- apps/web/public/health/old-banner.png
```

## Rename

```text
refactor(tooling): rename the configuration script

ADDED:
- tooling/sync-config.ts

DELETED:
- tooling/sync-config.mjs

EDITED:
- package.json
- AGENTS.md

Run the script with native TypeScript support and update every call site.
```
