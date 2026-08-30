# Step 3: Identify Candidate Increments

## Step goal

Give each approved epic a small set of coarse, revisable candidate increments.
These are roadmap prompts for later sprint planning, not ready-for-development
stories and not commitments to implementation detail.

## Mandatory rules

- Read this complete file before acting and process epic shards in index order.
- Collaborate with the user; do not silently invent priorities.
- Do not write Given/When/Then acceptance criteria, file-level code maps,
  dependency versions, or exhaustive edge cases here.
- Do not attempt to decompose the whole project to commit level.
- Do not create slice folders. Sprint planning owns just-in-time promotion into
  `03-slices/`.

## Process

For each epic:

1. Restate its user outcome, covered requirements, dependencies, and principal
   uncertainty.
2. Propose two to five candidate increments that would provide useful learning
   or value. Each is one sentence describing an observable outcome, not an
   implementation recipe.
3. Mark uncertain or distant candidates explicitly. Ordering beyond the next
   likely increment is directional and may change after feedback.
4. Ask the user whether the candidates are the right level of abstraction.
5. Replace `{{candidate_increments_N}}` and
   `{{dependencies_and_risks_N}}` in that epic shard.

If an epic cannot be described without detailed speculative design, record the
open question or research need instead of manufacturing stories.

## Completion check

Confirm that every shard:

- states an outcome;
- links to requirements without reproducing them;
- contains only coarse candidate increments;
- exposes dependencies and risks; and
- leaves commit-sized scope and acceptance criteria to sprint planning.

Display: `**Select an Option:** [A] Advanced Elicitation [C] Continue`

- **A**: Invoke `advanced-elicitation`, then redisplay the menu.
- **C**: Save the shards and read `./step-04-final-validation.md` fully.
- Anything else: respond, then redisplay the menu.

Always halt after displaying the menu.
