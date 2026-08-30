# Language conventions

Apply only entries relevant to the repository. Local conventions and configured tooling take precedence.

Use the language's native documentation form. Prefer semantic constraints, errors, side effects, ownership, lifecycle, concurrency, cancellation, units, ranges, compatibility, and security boundaries over duplicated type or signature information.

Common forms include:

- TypeScript and JavaScript: TSDoc or JSDoc for runtime errors, side effects, component behaviour, and asynchronous semantics.
- Python: the established docstring style for exceptions, mutation, I/O, context-manager ownership, iterator consumption, and sentinel semantics.
- Rust: `//!` and `///`, with `# Errors`, `# Panics`, `# Safety`, and runnable `# Examples` where required.
- Go: exported Go doc comments, error identity, blocking and cancellation behaviour, concurrency safety, and executable examples.
- C and C++: ownership, lifetime, nullability, buffers, aliasing, exceptions, thread safety, ABI, and template requirements.
- Java, Kotlin, C#, Swift, and similar languages: native documentation syntax for nullability, lifecycle, disposal, async behaviour, concurrency, and platform availability.
- Shell and build files: portability, quoting, privilege, environment, caching, generated outputs, and destructive effects.
- Schemas and configuration: descriptions for defaults, required fields, ranges, precedence, secrets, reload behaviour, compatibility, and deprecation.

In mixed-language repositories, use each language's native convention while keeping shared terminology and behavioural promises consistent across implementations, bindings, schemas, and examples.
