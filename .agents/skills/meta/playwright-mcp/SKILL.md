---
name: playwright-mcp
description: Use Playwright MCP and Playwright Test Agents to explore web applications, create executable test plans, generate Playwright tests, and heal failing tests. Use when browser-driven test discovery, test generation, selector verification, or repair is required. Keep MCP browser exploration separate from the repository's Playwright Utils implementation rules.
---

# Playwright MCP

Use the official Playwright MCP server for browser interaction through structured accessibility snapshots and testing tools. Use the three Playwright Test Agents as a deliberate workflow:

- **Planner** explores the application and writes a Markdown test plan.
- **Generator** turns the plan into executable Playwright tests and verifies selectors while generating them.
- **Healer** runs failing tests, investigates the current UI, proposes repairs, and reruns the affected tests within guardrails.

## Setup

The project MCP configuration uses:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

The checked-in agent definitions are the stable local integration. Read the relevant
reference before delegating work:

- [planner](references/agents/playwright_test_planner.toml) explores and saves plans.
- [generator](references/agents/playwright_test_generator.toml) converts plans into tests.
- [healer](references/agents/playwright_test_healer.toml) diagnoses and repairs failures.
- [seed fixture](references/fixtures/seed.spec.ts) provides the default environment seed.
- [test-plan guidance](references/test-plans.md) describes the plan directory.

Do not run `init-agents` as part of normal use. If Playwright changes its agent
protocol, compare the upstream definitions against these references and update
the skill deliberately.

## Agent workflow

1. Confirm the application, seed test, test environment, and any required authentication.
2. Ask Planner for a focused scenario or user-flow plan. Store plans in the repository's established test-plan location, commonly `specs/`.
3. Give Generator the plan and seed test. Generate tests in the repository's established test directory, commonly `tests/`.
4. Run the generated tests with the repository's configured test command.
5. Give Healer a specific failing test. Accept a repair only when the failure is understood and the resulting assertion still expresses the intended behaviour.
6. Re-run the relevant test and the appropriate wider suite.

Use [evaluation criteria](evals/playwright-test-agents.md) to assess generated
plans, tests, and repairs before accepting them.

## MCP interaction rules

- Use accessibility snapshots and Playwright testing tools for discovery and selector verification.
- Re-inspect the page after navigation, dialogs, menus, state changes, or failed interactions.
- Prefer role, label, text, and test-id locators that express user-visible intent.
- Capture the seed, plan, generated test, failure, and repair relationship in comments or filenames when the repository convention supports it.
- Never treat a healed test as proof that the product is correct; check whether the implementation or the test was wrong.
- Do not put credentials, private endpoints, personal data, or production exports in plans, tests, fixtures, or MCP prompts.

## Repository integration

When test generation is in scope, follow the repository's existing Playwright Utils mandate and test architecture. MCP is the browser-interaction mechanism; it does not override fixture, network interception, assertion, naming, or test-isolation rules.

Use the `playwright` CLI skill for direct terminal browser automation when Playwright Test Agents or MCP are not needed. Use `context7-mcp` for current Playwright API documentation questions, not for browser exploration.
