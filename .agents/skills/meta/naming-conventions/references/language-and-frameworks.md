# Language and framework conventions

Apply only the relevant sections. Project configuration and framework requirements override these defaults.

| Ecosystem | Common convention |
| --- | --- |
| TypeScript/JavaScript | `camelCase` values; `PascalCase` types; project-specific file casing. |
| Python | `snake_case` values and modules; `PascalCase` classes. |
| Rust | `snake_case` values and modules; `PascalCase` types; kebab-case Cargo packages. |
| Go | mixedCaps; exported names uppercase; preserve `ID`, `URL`, and `HTTP`. |
| Java/Kotlin | lower camel case values; upper camel case types; lowercase packages. |
| C#/.NET | camelCase locals; PascalCase public members; `Async` and `I` where conventional. |
| Swift | lower camel case values; upper camel case types; follow Swift API Design Guidelines. |
| Ruby | `snake_case`; `CamelCase`; predicate methods commonly end `?`. |
| PHP | Follow repository or PSR conventions and Composer namespaces. |
| Dart | lower camel case values; upper camel case types; lowercase-with-underscores files. |
| Elixir/Clojure | snake_case / kebab-case; predicate functions commonly end `?`. |
| PowerShell | Approved Verb-Noun commands and PascalCase parameters. |
| Shell | Existing portability and command conventions take priority; exported variables commonly use `UPPER_SNAKE_CASE`. |
| SQL | Database conventions and migration tooling control identifiers. |
| Solidity | mixedCase functions and variables; PascalCase contracts; ABI names are contracts. |
| Zig | camelCase functions and variables; PascalCase types. |

For React and TSX, use PascalCase noun components, `use...` hooks, and the repository's established event-prop conventions. Preserve framework-controlled names such as Next.js route, page, layout, loading, error, middleware, and configuration files. Never rename generated identifiers directly; change the canonical schema or generator input and regenerate.
