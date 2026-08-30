# Files, contracts, and tests

Follow language, framework, package-manager, build-system, and repository conventions for files and folders. Name them for responsibility or domain ownership; avoid vague containers unless they form a real abstraction. Preserve framework-controlled names, platform suffixes, migration numbering, and discovery patterns.

Before renaming packages, check imports, published names, workspace references, lockfiles, build outputs, containers, deployment configuration, documentation, and downstream consumers. Treat environment variables, CLI commands, configuration keys, API fields, database columns, storage keys, event topics, queues, and serialized fields as public or persisted contracts. Check aliases, schemas, migrations, compatibility, generated clients, caches, consumers, permissions, monitoring, and rollout requirements.

Never rename generated output directly. Update its canonical source and regenerate. Use the test runner's discovery rules. Name tests for their condition and expected behaviour, and distinguish fixtures, factories, mocks, fakes, stubs, spies, snapshots, and golden files according to repository meaning. Parameterized cases should expose the meaningful scenario.
