# Playwright Test Agents evaluation

Use this checklist when validating the local Planner, Generator, and Healer references.

## Planner

- Starts from the configured seed test and records the required starting state.
- Explores primary flows, validation, errors, boundaries, and relevant user roles.
- Produces independent scenarios with numbered steps and observable outcomes.
- Saves a focused Markdown plan under the established test-plan directory.
- Does not claim coverage for UI or behavior it did not inspect.

## Generator

- Uses the selected plan and seed without inventing unavailable setup.
- Verifies selectors and assertions against the live application through MCP.
- Produces one maintainable test per scenario with the repository's fixtures and naming rules.
- Uses user-facing locators and web-first assertions where appropriate.
- Preserves the intended behavior instead of encoding incidental markup or timing.

## Healer

- Reproduces the failure before changing the test.
- Separates product defects, environment failures, stale selectors, timing problems, and bad assertions.
- Makes the smallest reliable repair and explains its cause.
- Re-runs the affected test and the appropriate suite.
- Uses `test.fixme()` only when the test is correct, the product is demonstrably broken, and the reason is recorded beside the skipped behavior.

## Acceptance gate

Reject the result if it hides a product defect, weakens a meaningful assertion, adds arbitrary waits, uses prohibited credentials or private data, or cannot be traced from seed to plan to test to repair.
