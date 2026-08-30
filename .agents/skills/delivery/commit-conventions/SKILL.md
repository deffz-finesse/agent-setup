---
name: commit-conventions
description: Rules for git branching, staging, committing, and pull requests in this repository — atomic commits, Conventional Commits subject format, structured commit bodies, branch naming, and PR creation. Use before any git mutation — staging, committing, branching, pushing, or opening a pull request — even when only asked to draft a message.
---

# Git Commit Conventions

## Authority and scope

Create or mutate branches, commits, remotes, and pull requests only when
the user explicitly requests that operation. Drafting a proposed commit
message or pull-request body is read-only and does not authorize the
corresponding Git or GitHub mutation.

Use the `gh` skill for structured GitHub CLI reads, pagination, and explicit
repository targeting. If that skill or the required tooling is unavailable,
report the limitation instead of guessing from truncated output.

## Inspect before mutation

Review the relevant state before staging or committing:

```bash
git status
git diff
git diff --staged
git log --oneline -10
```

When a requested push or pull request involves a tracked branch, also
inspect whether it is ahead of or behind its remote. Refuse to stage
secrets, `.env` files, tokens, credentials, or real personal data. Prefer
explicit paths over `git add .`.

Never change Git configuration for the user. Avoid interactive flags that
the active harness cannot drive.

## Branches

Prefer these formats:

- `<type>/<issue-number>-<short-description>` when an issue exists
- `<type>/<short-description>` when no issue exists

Never commit or push directly to a protected branch. Check the repository's
actual branch policy or remote configuration when that matters; do not assume
that a local hook enforces protection.

## Atomic commits

One commit should represent one coherent change. Split mixed concerns
such as:

- a bug fix combined with a feature
- refactoring combined with behavior changes
- unrelated fixes
- formatting combined with logic

When splitting is warranted:

1. Explain the split briefly.
2. Stage explicit paths for each unit.
3. Commit in an order that keeps every intermediate commit coherent. A
   useful default is fix, feature, refactor, test, documentation, then
   tooling.
4. Complete the requested sequence without leaving an agreed unit
   uncommitted.

## Commit subjects

Follow Conventional Commits. Allowed types are `feat`, `fix`, `docs`,
`test`, `refactor`, `perf`, `build`, `ci`, `chore`, `revert`, and
`security`.

- Keep the subject within 100 characters.
- Use imperative mood: `feat: add session expiry`, not `added` or `adds`.
- Use a specific description; avoid subjects such as `fix bug` or
  `changes`.
- Use a lowercase type and an optional scope when it clarifies the area.
- Follow recent repository scope conventions instead of inventing a
  taxonomy.
- Do not end the subject with a period.
- Do not add agent attribution or `Co-authored-by` trailers for coding
  agents.

If repository hooks or CI checks are configured, honor them. The remaining
language conventions are review policy.

## Commit bodies

List the staged paths for that commit under `ADDED:`, `EDITED:`, and
`DELETED:`; omit only categories that are empty. Derive the list from
`git diff --staged --name-status`, not from the whole working tree.

- Use one repository-relative path per line.
- Represent a rename as deleted plus added, or as
  `EDITED: old-path → new-path` when the rename is the entire change.
- When five or more files under one directory share a change kind, fold
  that category to the narrowest accurate `path/**` entry.
- Do not combine added, edited, and deleted files into one folded entry.

After the path inventory, explain why the change was necessary when the
reason is not obvious from the subject. Add `Closes #123`, `Fixes #456`,
or `BREAKING CHANGE: ...` when applicable.

Use a quoted heredoc when constructing a multiline message so the shell
cannot expand its contents accidentally:

```bash
git commit -m "$(cat <<'EOF'
feat(web): add session expiry banner

ADDED:
- apps/web/src/components/session-banner.ts

EDITED:
- apps/web/src/routes/root.ts

Explain the reason for the change when it is not obvious.
EOF
)"
```

Full worked examples for every commit type (feature, bug fix,
documentation, tooling, refactor, test, security, folder folding,
rename) are in `references/commit-examples.md` — read it when composing
a body, not before.

## Amend, hooks, and history rewriting

- Honor repository hooks. Do not use `--no-verify` merely to make a
  commit pass. Do not disable signing unless the user explicitly requests
  it.
- Amend only when the user requests it, the current `HEAD` was created
  during the active conversation, and it has not been pushed.
- When a hook rejects a commit, fix the cause and create the requested
  commit; do not amend a commit that was never created.
- Rewrite a published feature branch only with explicit approval and
  `--force-with-lease`.
- Never force-push a protected branch.
- After committing, inspect `git status` and `git log --oneline -1`. If a
  hook rewrote files after a successful commit, follow the amend
  restrictions above before including them.

## Pull requests

Push or create a pull request only when the user asks. Push the current
feature branch with `git push -u origin HEAD`, then use the repository
pull-request template and the `gh` skill. Match
draft-versus-ready status to the request. Never merge unless explicitly
authorized.

```bash
gh pr create --title "feat(web): add session expiry banner" --body "$(cat <<'EOF'
## Summary

- Add a warning before the authenticated session expires.

## Test plan

- [ ] Run the authoritative project validation command.
EOF
)"
```
