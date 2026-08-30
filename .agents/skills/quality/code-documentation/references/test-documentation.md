# Test documentation

Treat tests as executable evidence of behaviour. They support public documentation but do not replace it.

Inspect tests when changes affect public behaviour, errors, validation, boundaries, configuration defaults, serialization, state transitions, concurrency, security, performance, regressions, compatibility, or deprecation.

Prefer test names that state the condition and expected behaviour. Comment only unusual setup: race reproduction, fake clocks, platform setup, protocol fixtures, malformed input, security regressions, tolerances, snapshot normalization, external failure simulation, retry timing, or cleanup that prevents contamination.

Document shared fixtures and helpers when their defaults, ownership, cleanup, transaction boundaries, clock behaviour, randomness, network access, filesystem effects, process lifetime, authentication state, hidden retries, or expensive setup are not obvious. Use synthetic or sanitized data; never put credentials, private endpoints, personal data, customer exports, or production secrets in fixtures.

Regression tests should make the previously failing condition recoverable from their name, setup, or a concise issue reference. Generated snapshots and golden files are outputs: update their canonical input or regeneration process.

Use executable examples when supported. Update testing guides when commands, dependencies, suites, markers, fixtures, environments, or CI behaviour change. Do not turn an internal implementation detail into a compatibility promise merely because a test asserts it.
