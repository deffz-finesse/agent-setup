# Semantic naming rules

Use these rules after applying repository, language, framework, and external-contract requirements.

## Functions and methods

Function names should usually begin with a verb matching their main observable behaviour: `get` returns an available value, `find` searches with expected absence, `require` fails when a value is absent, `create` produces a new resource, `build` assembles a value, `read` reads input or storage, `load` retrieves and prepares data, `fetch` retrieves remotely, `parse` converts serialized input, `validate` checks without repairing, `normalize` canonicalizes equivalent forms, `resolve` determines a final value, `update` changes an existing value, and `delete` or `remove` uses the domain distinction.

Report names that lie about effects, such as a getter that creates records or a validator that mutates input. `process`, `run`, `execute`, `manage`, and `handle` are acceptable when the domain or framework gives them a precise meaning.

## Booleans and collections

Boolean names should read as claims or questions in the language's natural style (`is`, `has`, `can`, `should`, `supports`, `requires`). Avoid double negatives. Singular names represent one value; plural or established collection nouns represent several values. Do not add `list`, `array`, `map`, or `set` unless representation matters to callers.

## Units, state, and types

Make units explicit when context or a strong unit type does not make them unambiguous. Distinguish counts, indices, offsets, sizes, limits, percentages, timestamps, durations, and identifiers. Names should distinguish requested/resolved, raw/parsed, supplied/defaulted, cached/authoritative, and other meaningful states. Use representation suffixes only when they mark a real boundary such as `Request`, `Response`, `Options`, `Command`, `Event`, or `Result`.

## Abbreviations and families

Prefer established domain and ecosystem abbreviations and follow the target language's initialism casing. Related names should share the same domain noun and intentional distinctions. Generic words such as `data`, `info`, `result`, `service`, `manager`, and `helper` are not automatically wrong; review whether their scope supplies enough meaning.

Use consistent spelling, plurality, tense, and compound forms. Preserve externally controlled spellings at the boundary.
