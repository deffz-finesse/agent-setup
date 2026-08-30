---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use only when the user explicitly asks to be grilled or uses a clear grill trigger.
---

# Grilling

This is an explicit opt-in escalation for stress-testing a plan, decision, or
idea. For ordinary ambiguity, use `requirement-interrogation`; for refinement
of an existing output, use `advanced-elicitation`.

Interview the user relentlessly until you reach a shared understanding. Map
the topic as a **design tree**: every decision branches into the decisions that
depend on it.

Work the tree in rounds. The **frontier** is every decision whose prerequisites
are settled: the questions that can be asked now without guessing at answers
that have not been given. Ask the whole frontier in one round, number each
question, give a recommended answer, and wait for the user's answers before
continuing.

Format a round like this:

```text
❓ Q1 — <question title>: <question body, including choices when useful>

➡️ Recommended answer: <recommendation and reason>

---

❓ Q2 — <question title>: <question body>

➡️ Recommended answer: <recommendation and reason>
```

Each round reshapes the tree. Settled decisions push the frontier outward;
questions that depend on another unanswered question belong to a later round.

Finding facts is the agent's job, not the user's. Inspect the repository, tools,
and available documentation when a question depends on an environmental fact.
Ask the user only for decisions, preferences, or information that cannot be
discovered safely.

The session ends when every relevant branch has been visited and nothing
important remains silently assumed. Do not implement the result until the user
confirms that shared understanding has been reached.
