---
name: gh
description: Structured GitHub CLI (gh) usage — JSON output over column-parsing, explicit pagination, and explicit repository targeting. Use for any gh read — pull requests, issues, runs, releases, repo info — and referenced by commit-conventions for PR creation.
---

# gh (GitHub CLI)

This is `cli/cli`'s `gh` — the official GitHub CLI, verified against
`gh version 2.46.0`. This skill covers reading GitHub data reliably.
Creating or mutating anything (PRs, issues, comments) is
`commit-conventions`' authority-and-scope rule: only when the user
explicitly asks.

## Three rules, always

1. **`--json <fields>`, never parse column output.** Every `gh <noun>
   list`/`view` command supports `--json`. Column-formatted default output
   is for humans and reflows across versions/terminal widths — do not
   parse it.
2. **Don't guess field names — ask `gh` for them.** Run the command with
   `--json` and no value; it prints every valid field for that command
   and exits. Do this before guessing.

   ```bash
   gh pr list --json
   gh repo view --json
   ```

3. **Set `-R owner/repo` and `--limit` explicitly**, don't rely on
   defaults. `-R`/`--repo` avoids depending on the working directory's
   git remote — required whenever operating across repos or when
   explicitness matters. Every `list` command defaults to a small
   `--limit` (20–30) that silently truncates; set it explicitly for
   anything that needs completeness.

## Quick patterns

```bash
# Full field list for a command (run first, don't guess)
gh pr list --json

# Structured, explicit, complete
gh pr list -R owner/repo --json number,title,author,state --limit 100
gh issue list -R owner/repo --json number,title,labels,state --limit 100
gh run list -R owner/repo --json databaseId,status,conclusion,workflowName --limit 50

# Extract a specific value with --jq instead of piping to jq separately
gh api repos/{owner}/{repo}/issues --jq '.[].title'

# Every page, not just the first
gh api repos/{owner}/{repo}/issues --paginate

# Auth state — check before assuming a call will succeed
gh auth status
```

Full per-command reference (pr, issue, run, release, repo, api) is in
`references/gh-cli-reference.md` — read the section for the command
being used, not the whole file.
