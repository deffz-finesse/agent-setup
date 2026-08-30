# Documentation examples

Adapt the principle rather than copying exact syntax.

## Document semantics beyond the type

```ts
/**
 * Returns `null` when the account does not exist.
 *
 * Retries transient transport failures. Authentication failures are returned
 * immediately because another attempt cannot succeed with the same credentials.
 */
async function fetchUser(id: UserId): Promise<User | null> {
  return retryTransient(() => directory.fetch(id));
}
```

The return type does not explain retry behaviour or distinguish absence from failure. Adding a parameter tag that merely repeats the type adds no useful information.

## Put rationale beside the constraint

```python
# The upstream signature format accepts whole Unix seconds only.
issued_at = time.time_ns() // 1_000_000_000
```

Explain the constraint, not the arithmetic visible in the expression.

## State ownership and safety obligations

```rust
/// Creates a view over `ptr` without copying.
///
/// # Safety
///
/// `ptr` must remain valid and immutable for `len` bytes until the returned
/// view is dropped. Another owner must not free the memory during that period.
pub unsafe fn borrowed_view(ptr: *const u8, len: usize) -> View<'static> {
    // ...
}
```

The useful content is the obligation the type system cannot enforce.

## Prefer enforcement over prose

Instead of documenting that a timeout must be positive and measured in milliseconds, use a constrained representation such as `require_positive_timeout()` when it fits the task. Retain a comment only when the reason remains non-obvious.

## Tests can document behaviour

```python
def test_retries_transport_errors_but_not_authentication_errors():
    ...
```

Explain unusual setup, deliberately malformed fixtures, and temporary workarounds only when names and assertions cannot recover the reason.
