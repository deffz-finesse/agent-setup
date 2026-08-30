---
name: context7-mcp
description: Use Context7 for current library, framework, and API documentation when setup or code examples depend on a named package. Do not use it for general research or repository history.
---

When the user asks about a library, framework, or API, use the configured
Context7 MCP server to fetch current documentation instead of relying on
training data. The server is declared project-locally in `.mcp.json` for
Claude Code and `.codex/config.toml` for Codex. If the server or its tools are
unavailable, say so and use the library's official documentation through the
`research` workflow; do not invent Context7 results.

This route is required during Research and Plan whenever a named library,
framework, SDK, or API affects the question or design. Resolve the library and
query the relevant current documentation before relying on general web search,
memory, or an unverified package assumption.

It is normally handed off from [`deep-recon`](../../planning/deep-recon/SKILL.md),
[`spec`](../../planning/spec/SKILL.md), or
[`architect`](../../agents/architect/SKILL.md). Return the resolved library ID, queried
concept, and relevant version to the calling skill so the result can be cited
in the owning artifact.

## When to Use This Skill

Activate this skill when the user:

- Asks setup or configuration questions ("How do I configure Next.js middleware?")
- Requests code involving libraries ("Write a Prisma query for...")
- Needs API references ("What are the Supabase auth methods?")
- Mentions specific frameworks (React, Vue, Svelte, Express, Tailwind, etc.)

## How to Fetch Documentation

### Step 1: Resolve the library ID

Use the configured Context7 library-resolution tool (`resolve-library-id`) with:

- `libraryName`: The library name extracted from the user's question
- `query`: What to look up in the library's documentation (improves relevance ranking)

### Step 2: Select the best match

From the resolution results, choose based on:

- Exact or closest name match to what the user asked for
- Higher benchmark scores indicate better documentation quality
- If the user mentioned a version (e.g., "React 19"), prefer version-specific IDs

### Step 3: Fetch the documentation

Use the configured Context7 documentation tool (`query-docs`) with:

- `libraryId`: The selected Context7 library ID (e.g., `/vercel/next.js`)
- `query`: What to look up in the library's documentation, scoped to a single concept

If the user's question spans multiple distinct concepts (e.g. routing and
auth and caching), make a separate `query-docs` call per concept with the
same library ID, unless the question is about how the concepts interact —
combined queries dilute ranking and return shallow results for each topic.

### Step 4: Use the Documentation

Incorporate the fetched documentation into your response:

- Answer the user's question using current, accurate information
- Include relevant code examples from the docs
- Cite the library version when relevant
- Keep the fetched library documentation separate from repository-specific
  conventions and from general web research.

## Guidelines

- **Be specific**: Describe what to look up in the library's documentation, but keep each query to a single concept
- **One topic per query**: Split multi-topic questions into separate `query-docs` calls — resolve the library ID once, then query per concept, unless the question is about how the concepts interact
- **Version awareness**: When users mention versions ("Next.js 15", "React 19"), use version-specific library IDs if available from the resolution step
- **Prefer official sources**: When multiple matches exist, prefer official/primary packages over community forks
