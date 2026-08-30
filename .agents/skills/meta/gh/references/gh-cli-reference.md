# gh CLI reference

Verified against `gh version 2.46.0` — every flag below was checked
against this repo's installed `gh`, not recalled from memory. Run
`gh <command> --help` for the authoritative current flags if this
version drifts; run `gh <command> --json` with no value to get the
current field list for any command that supports it.

Structured-output support is **not uniform** across `gh` — three
different patterns exist, and guessing wrong is the main failure mode
this reference prevents:

| Pattern | Commands |
| --- | --- |
| `--json fields` (most common) | `pr`, `issue`, `run`, `release`, `repo view`, `search *`, `workflow list`, `label list`, `secret list`, `variable list`, `codespace list` |
| `--format json` (different flag name, same idea) | `project`, `project item-list` |
| **No structured output at all** | `gh pr checks`, `gh gist list`, `gh org list` — column output is the only form |

Mutating anything below (`create`, `edit`, `delete`, `merge`, `close`,
`set`, `disable`, etc.) is gated by `commit-conventions`' authority
rule: only run it when the user explicitly asked for that operation.
Drafting the command to show the user is not authorization to run it.

## Contents

**Core:** [auth](#auth) · [browse](#browse) · [codespace](#codespace) ·
[gist](#gist) · [issue](#issue) · [org](#org) · [pr](#pr) ·
[project](#project) · [release](#release) · [repo](#repo)

**GitHub Actions:** [cache](#cache) · [run](#run) · [workflow](#workflow)

**Additional:** [alias](#alias) · [api](#api) ·
[completion](#completion) · [config](#config) · [extension](#extension) ·
[gpg-key](#gpg-key) · [label](#label) · [ruleset](#ruleset) ·
[search](#search) · [secret](#secret) · [ssh-key](#ssh-key) ·
[status](#status) · [variable](#variable)

---

## auth

**For:** authentication state — logging in/out, checking who you're
authenticated as, token access.

**When:** check `gh auth status` before a command whose failure could be
either "not authenticated" or "genuinely no results" — resolves the
ambiguity for free.

```bash
gh auth status              # per-host auth state, read-only, cheap
gh auth login                # interactive/flag-driven login — user-initiated only
gh auth token                 # print the current token — treat the output as a live credential, never log or paste it
gh auth switch                # change active account when multiple are logged in
```

`gh auth token` prints a real secret to stdout. Never echo it into a
commit, issue, log file, or anywhere it could persist.

## browse

**For:** opening the repo (or a specific file/PR/issue) in a web
browser.

**When:** essentially never from an agent context — it opens a GUI
browser window, which doesn't help a non-interactive session. Mention it
exists; don't reach for it.

```bash
gh browse                     # opens repo home in browser
```

## codespace

**For:** managing GitHub Codespaces (cloud dev environments) — list,
create, SSH into, stop.

**When:** only if the user is explicitly working with Codespaces. Read
form is `--json`-capable:

```bash
gh codespace list --json name,repository,state,gitStatus --limit 50
```

Mutating subcommands (`create`, `delete`, `stop`, `rebuild`) provision or
tear down real cloud compute — treat as a mutation requiring explicit
request, same as any other.

## gist

**For:** managing gists (standalone shareable snippets, separate from
repositories).

**When:** sharing a snippet outside repo context, or reading one the
user references.

```bash
gh gist list --limit 50       # NO --json support — column output only
gh gist view <id>
gh gist create file.md         # mutation — explicit request only
```

## issue

**For:** the full issue lifecycle — read, comment, label, link to
branches, close/reopen, transfer.

**When:** any issue read or (on explicit request) write.

```bash
gh issue list -R owner/repo --json number,title,labels,state,assignees --limit 100
gh issue view 45 -R owner/repo --json title,body,state,comments
gh issue create -R owner/repo --title "..." --body "..."   # mutation
gh issue develop 45 -R owner/repo                             # link/create a branch for an issue
```

Common `--json` fields: `number`, `title`, `body`, `state`, `labels`,
`assignees`, `milestone`, `comments`, `createdAt`, `closedAt`.

## org

**For:** listing organizations the authenticated user belongs to.

```bash
gh org list --limit 100       # NO --json — column output only
```

## pr

**For:** the full pull-request lifecycle — the one most commit/PR work
touches.

**When:** any PR read; creation only via `commit-conventions`' PR
section on explicit request.

```bash
gh pr list -R owner/repo --json number,title,author,state,labels --limit 100
gh pr view 123 -R owner/repo --json title,body,state,mergeable,reviews
gh pr checks 123 -R owner/repo --required   # NO --json — the one PR subcommand without it
gh pr diff 123 -R owner/repo                 # unified diff, plain text by design
gh pr create --title "..." --body "..."      # mutation — see commit-conventions
gh pr merge 123 --squash --delete-branch     # mutation — never without explicit authorization to merge
gh pr review 123 --approve                   # mutation — approving/requesting changes is a real review action
```

Common `--json` fields: `number`, `title`, `author`, `state`, `labels`,
`body`, `isDraft`, `mergeable`, `mergeStateStatus`, `reviews`,
`latestReviews`, `commits`, `files`, `additions`, `deletions`,
`changedFiles`, `headRefName`, `baseRefName`, `createdAt`, `closedAt`,
`mergedAt`, `mergedBy`.

`gh pr merge` flags are mutually exclusive strategies (`--merge`,
`--squash`, `--rebase`) plus `--auto` (merge once checks pass) and
`-d`/`--delete-branch`. Never invoke without the user explicitly
authorizing a merge — this is the single most consequential mutation in
this whole reference.

## project

**For:** GitHub Projects (v2) — boards, fields, items.

**When:** the user is explicitly using Projects for tracking.

```bash
gh project list --owner org-or-user --format json --limit 100   # --format, not --json
gh project item-list <number> --owner org-or-user --format json --limit 100
```

Structured output here uses `--format json`, not `--json fields` — the
one command family in this reference where the flag name itself
differs, not just its presence.

## release

**For:** GitHub Releases — versions, changelogs, downloadable assets.

```bash
gh release list -R owner/repo --json tagName,name,createdAt,isDraft,isPrerelease --limit 30
gh release view v1.2.0 -R owner/repo --json body,assets,tagName
gh release download v1.2.0 -R owner/repo    # read-only despite the verb — fetches assets locally
gh release create v1.2.0 --notes "..."       # mutation
```

`--order asc|desc` controls sort (default `desc`, newest first).

## repo

**For:** repository-level operations — view metadata, clone, fork,
create, archive, configure defaults.

```bash
gh repo view owner/repo --json description,defaultBranchRef,isArchived,forkCount,diskUsage
gh repo list owner-or-org --limit 100
gh repo clone owner/repo                      # read-only despite mutating the local filesystem outside the repo
gh repo create name --private                 # mutation — creates a real remote repository
gh repo fork owner/repo                        # mutation — creates a real remote repository
```

Common `gh repo view` fields: `description`, `defaultBranchRef`,
`isArchived`, `isEmpty`, `hasIssuesEnabled`, `hasWikiEnabled`,
`forkCount`, `diskUsage`, `fundingLinks`.

---

## cache

**For:** GitHub Actions cache entries (build/dependency caches attached
to the repo).

```bash
gh cache list -R owner/repo --limit 100
gh cache delete <cache-id> -R owner/repo      # mutation
```

## run

**For:** Actions workflow _run_ history and logs — did CI pass, what
failed, download artifacts.

```bash
gh run list -R owner/repo --json databaseId,status,conclusion,workflowName,headBranch --limit 50
gh run view <run-id> -R owner/repo --json status,conclusion,jobs
gh run watch <run-id> -R owner/repo            # blocks until the run finishes — only when the user wants to wait live
gh run rerun <run-id> -R owner/repo             # mutation
gh run cancel <run-id> -R owner/repo             # mutation
```

`--status` filters without needing `--json` for a coarse check:
`queued`, `in_progress`, `completed`, `success`, `failure`, `cancelled`,
and others.

## workflow

**For:** the workflow _definitions_ themselves (as opposed to `run`'s
individual executions) — list, enable/disable, manually dispatch.

```bash
gh workflow list -R owner/repo --json id,name,state --limit 50
gh workflow view <id-or-name> -R owner/repo    # summary — no --json flag on view itself
gh workflow run <id-or-name> -R owner/repo      # mutation — triggers a real workflow_dispatch event
gh workflow disable <id-or-name> -R owner/repo   # mutation
```

---

## alias

**For:** local shortcuts for `gh` command invocations — a user
convenience feature, not a data source.

```bash
gh alias list
gh alias set pv 'pr view'                      # mutation of local gh config, not the repo
```

## api

**For:** anything not covered by a dedicated subcommand — direct REST or
GraphQL access, authenticated the same way as `gh` itself. The escape
hatch when a purpose-built command doesn't exist yet.

```bash
gh api repos/{owner}/{repo}/issues --jq '.[].title'
gh api repos/{owner}/{repo}/issues --paginate    # every page, not just the first
gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes { name }
        pageInfo { hasNextPage endCursor }
      }
    }
  }'
```

`--paginate` on a GraphQL query requires the query itself to accept
`$endCursor: String` and read `pageInfo` — it does not paginate an
arbitrary query automatically. `-X` sets the HTTP method for REST writes
(`POST`, `PATCH`, `DELETE`, `PUT`) — a mutation the moment it's anything
but `GET`, gated the same as every other mutation in this reference.

## completion

**For:** generating shell completion scripts (bash/zsh/fish/PowerShell)
for interactive terminal use. Not relevant to an agent session.

## config

**For:** `gh`'s own local configuration (default editor, git protocol,
prompt behavior) — not repository or GitHub state.

```bash
gh config list
gh config get git_protocol
gh config set git_protocol ssh                 # mutation of local gh config
```

## extension

**For:** third-party `gh` extensions — installing, listing, removing
community-built subcommands.

```bash
gh extension list
gh extension search <term>
gh extension install owner/gh-extension-name    # mutation — installs and runs third-party code
```

Installing an extension runs code from outside GitHub's own CLI —
treat it with the same scrutiny as installing any other unreviewed
dependency, not as a routine read.

## gpg-key

**For:** GPG keys attached to the authenticated GitHub account (commit
signature verification).

```bash
gh gpg-key list
gh gpg-key add key.gpg                          # mutation — changes account security config
```

## label

**For:** issue/PR labels at the repository level — distinct from
applying a label to one issue (that's `gh issue edit --add-label`).

```bash
gh label list -R owner/repo --json name,color,description --limit 100
gh label create bug -R owner/repo --color FF0000  # mutation
gh label clone owner/source-repo -R owner/dest-repo  # mutation — copies a repo's whole label set
```

## ruleset

**For:** repository/organization branch-protection rulesets — read-only
in this CLI (no create/edit subcommand; rulesets are managed via the web
UI or API).

```bash
gh ruleset list -R owner/repo --limit 30
gh ruleset check <branch> -R owner/repo         # what rules would apply to this branch
```

`--org` requires the `admin:org` token scope (`gh auth refresh -s
admin:org`) — expect a permissions error without it, not a bug.

## search

**For:** searching across GitHub, not limited to one repository —
distinct from `pr list`/`issue list`, which only search within a
specified repo.

```bash
gh search prs "is:open author:@me" --json number,title,repository --limit 50
gh search issues "label:bug" -R owner/repo --json number,title --limit 50
gh search repos "language:typescript stars:>1000" --json fullName,stargazersCount --limit 50
gh search code "TODO" -R owner/repo --json path,repository --limit 50
gh search commits "fix:" -R owner/repo --json sha,commit --limit 50
```

All five `search` subcommands support `--json`, `--limit`, and `-R`
consistently — the most uniform command family in this reference.

## secret

**For:** GitHub Actions secrets (encrypted, write-only values) at repo
or org level.

```bash
gh secret list -R owner/repo --json name,updatedAt
gh secret set NAME -R owner/repo --body "value"   # mutation — a real credential write
```

`gh secret list` can never show secret values — GitHub doesn't expose
them once set, by design. Don't expect or request one.

## ssh-key

**For:** SSH keys attached to the authenticated GitHub account.

```bash
gh ssh-key list
gh ssh-key add key.pub                          # mutation — changes account security config
```

## status

**For:** a cross-repository summary — assigned issues, review requests,
and mentions across every repo you have access to, in one call.

```bash
gh status                                        # no --json, no --limit — a fixed personal digest
```

Useful as a fast orientation check ("what's relevant to me right now")
before drilling into any specific repo's `issue`/`pr` commands.

## variable

**For:** GitHub Actions variables (plaintext config values, distinct
from `secret`'s encrypted ones) at repo or org level.

```bash
gh variable list -R owner/repo --json name,value,updatedAt
gh variable set NAME -R owner/repo --body "value"   # mutation
```

Unlike `secret`, `variable list --json` does expose the actual value —
these are meant to be non-sensitive config, not credentials. Don't put a
real secret in a `variable`.
