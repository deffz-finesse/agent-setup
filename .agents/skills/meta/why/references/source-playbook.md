# Source playbooks

The `why` skill always has source-control evidence through `git` and `gh`. Other evidence sources are discovered from the active client's configured MCPs at runtime. This template does not ship playbooks for SaaS integrations it does not configure.

| Category | Local playbook | Runtime source |
| --- | --- | --- |
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler). It uses only sources available in the active client.
