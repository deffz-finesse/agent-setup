# Incident & Postmortem Context

This is not a separate source; it is a cross-cutting angle. Incidents often motivate defensive code, so when the target looks defensive (null checks, retries, timeouts, rate limits, feature flags, or similar), hunt for incident history using only sources available in the active client.

- Search source-control history for incident, outage, rollback, revert, defensive-check, and reliability language.
- Search any configured issue tracker, documentation system, chat system, observability platform, error tracker, or analytics system using its native tool descriptions and query syntax. Do not assume provider-specific tool names or channel conventions.
- If an incident record is found, fetch the full record and inspect its timeline, root cause, and action items for links to the target code.
- Record unavailable sources as explicit gaps. A correlation across independent available sources is stronger evidence, but it is not proof of causation.

Use this angle when the code's defensive character makes an incident-driven origin plausible. Skip it for code that does not look defensive.
