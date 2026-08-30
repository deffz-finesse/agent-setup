# Documentation locations

Use the narrowest existing canonical location for information changed by code. Prefer repository equivalents over adding conventional filenames for appearance alone.

Check README and contributor documentation for installation, supported environments, examples, setup, tests, formatting, generated files, development workflow, and releases. Check architecture records for stable boundaries and important data flow. Check schemas and interface definitions for APIs, CLI behaviour, configuration, migrations, events, and compatibility.

Update operator documentation when changes affect deployment, migrations, rollback, health checks, alerts, logs, metrics, tracing, backups, resource limits, scheduled jobs, or recovery.

Inspect existing Markdown, prose, link, spelling, documentation-generation, doctest, example, schema-generation, and CI tooling before adding or changing documentation. Use configured versions and commands. Do not introduce another documentation system without a task requirement.

Before finishing, check whether the change affects user workflows, public contracts, setup, testing, release, deployment, recovery, configuration, data shape, permissions, compatibility, schemas, diagrams, examples, fixtures, or generated references. Update only locations whose readers would otherwise receive incomplete or false guidance.
