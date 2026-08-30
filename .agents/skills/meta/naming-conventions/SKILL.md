---
name: naming-conventions
description: Choose, review, and safely rename identifiers, types, functions, components, tests, files, folders, packages, commands, configuration keys, environment variables, database fields, API fields, events, and other named software concepts across programming languages. Use whenever code-bearing work creates or changes a name, when reviewing naming quality or terminology consistency, or when a rename may affect public, persisted, serialized, generated, or framework-controlled contracts. Follow repository, language, framework, external-contract, and domain terminology before general preferences.
---

# Naming conventions

Choose names that tell the truth about a concept's meaning, behaviour, scope, lifecycle, and ownership. Do not impose one language's casing or framework conventions on another.

## Establish authority

Resolve naming rules in this order:

1. Language syntax and compiler requirements.
2. Framework, build-system, platform, and code-generation requirements.
3. External API, protocol, database, serialization, filesystem, and deployment contracts.
4. Explicit repository standards, linters, schemas, and contributor instructions.
5. Existing public terminology and compatibility commitments.
6. Official language, framework, library, and package terminology.
7. Product and domain vocabulary.
8. Consistent nearby code.
9. General readability guidance from this skill.

Do not report controlled names as violations. If an external name conflicts with internal conventions, preserve it at the boundary and map it to an internal name when the translation is worth the cost.

Inspect configured naming rules before proposing changes. Relevant sources include formatter and linter configuration, compiler settings, schemas, code generators, framework conventions, style guides, public documentation, tests, and nearby code.

## Set the scope

For a code change, review names introduced or materially affected by the task. Inspect related names only as needed to detect contradictions, collisions, broken families, or unsafe renames. Do not turn a focused change into a repository-wide terminology rewrite.

For a naming audit, search definitions, references, exports, schemas, configuration, documentation, tests, fixtures, generated sources, and persisted contracts. Distinguish definite problems from subjective alternatives.

If the task is review-only, report findings without renaming files or symbols.

## Naming workflow

1. Identify what the thing is, what it does, who uses it, and how long the name must remain stable.
2. Determine whether another system controls the name.
3. Find the repository's casing, vocabulary, suffix, prefix, and file-placement conventions.
4. Check the name against its actual type, behaviour, effects, cardinality, units, optionality, lifecycle, and visibility.
5. Search for the same concept under other names and different concepts under similar names.
6. Choose the shortest name that remains precise in its real scope.
7. Assess rename impact before changing public, persisted, serialized, generated, or operational names.
8. Update related name families, references, tests, documentation, schemas, migrations, and generated sources when authorized.
9. Run relevant formatters, linters, type checks, tests, schema validation, and generators.

## Core qualities

A strong name is:

- accurate about behaviour and side effects;
- specific enough for its scope;
- consistent with the domain and nearby code;
- searchable without producing unrelated matches;
- grammatical when read in use;
- distinct from neighbouring concepts;
- stable at the boundary where consumers depend on it.

Prefer domain nouns and precise verbs. Avoid names that are clever, misleading, needlessly abbreviated, decorated with type information, or so generic that readers must inspect the implementation to understand them.

Do not apply a universal character limit. A three-line local scope can support a short name. A public cross-package contract usually needs more precision.

## Semantic checks

Confirm that names agree with:

- singular or plural cardinality;
- collection versus individual value;
- units, coordinate systems, time bases, and precision;
- optional, missing, empty, default, and sentinel states;
- synchronous, asynchronous, network, storage, and cached behaviour;
- creation, lookup, parsing, validation, normalization, mutation, and deletion;
- ownership, borrowing, lifecycle, visibility, and mutability;
- request, response, command, event, record, entity, model, and view representations;
- error, retry, cancellation, and partial-success behaviour.

Read [references/semantic-rules.md](references/semantic-rules.md) when choosing verbs, booleans, collections, units, types, abbreviations, or related name families.

## Language and framework rules

Do not use a universal casing table. Read [references/language-and-frameworks.md](references/language-and-frameworks.md) for the languages and frameworks present in the task. Apply only the relevant sections.

Framework-specific forms such as React hooks, Next.js routes, Rails conventions, Django settings, test discovery names, generated bindings, and platform prefixes override general preferences when required.

## Files, contracts, and tests

Read [references/files-contracts-and-tests.md](references/files-contracts-and-tests.md) when naming or renaming files, folders, packages, tests, fixtures, commands, environment variables, configuration keys, database fields, events, API fields, assets, or generated outputs.

Treat public and persisted renames as compatibility changes. Do not assume a project-wide search and replace is safe.

## Collision and terminology review

Classify findings accurately:

| Classification | Meaning |
| --- | --- |
| Collision | The same name represents different concepts in overlapping scope. |
| Near collision | Similar names represent different concepts and invite confusion. |
| Terminology fragmentation | Different names represent the same concept without a useful distinction. |
| Broken family | Related names use inconsistent nouns, verbs, prefixes, or suffixes. |
| Scope-safe reuse | The same short name appears in separate scopes where meaning remains clear. |
| External exception | A controlled name differs from internal convention by requirement. |

Do not report scope-safe reuse or external exceptions as violations.

When several names compete, prefer the one that is more semantically accurate, more public, more widely used, older at a compatibility boundary, aligned with product vocabulary, or required by an external contract. These factors require judgment rather than mechanical scoring.

Use [references/review-checklist.md](references/review-checklist.md) for full audits and rename planning.

## Avoid mechanical overreach

- Do not rename a clear name only to satisfy personal taste.
- Do not introduce a naming linter merely because one name needs improvement.
- Do not encode language types into names unless the ecosystem requires it.
- Do not add prefixes or suffixes that repeat the enclosing namespace, module, type, or folder.
- Do not ban a word globally when a precise compound uses it correctly.
- Do not normalize external names across a boundary that must preserve them.
- Do not edit generated output. Change its canonical source and regenerate.
- Do not rename public or persisted contracts without migration and compatibility planning.
