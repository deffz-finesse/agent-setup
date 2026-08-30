# Step 4: Final Validation

## Step goal

Validate that the roadmap covers the agreed project outcomes while remaining
deliberately rough enough to evolve through implementation feedback.

## Validation

Read the index, requirements inventory, and every epic shard in index order.
Check all of the following:

1. Every functional requirement maps to at least one epic horizon. Coverage at
   this stage does not require a prewritten implementation story.
2. Each epic describes a meaningful outcome or learning boundary rather than a
   technical layer.
3. Dependencies and risks are visible, and no later epic is falsely presented
   as fully designed.
4. Candidate increments are short outcome statements. Fail validation if the
   shards contain detailed acceptance criteria, file-by-file implementation
   plans, exhaustive story inventories, or other premature commitments.
5. The next likely horizon is clear enough for `sprint-planning` to select a
   few coordinated, commit-sized slices just in time.
6. The index, inventory, and shards contain no unresolved template
   placeholders.

If validation fails, return to the owning step and refine with the user. Do not
paper over missing decisions.

When validation passes, append a finalization event to `.memlog.md`, register
the index, inventory, memlog, and epic shards as `current` with
`run_state.py add-artifact`, and advance the run to `overall-plan` if needed.

Display: `**Roadmap validation complete. [C] Complete Workflow**`

Halt. On **C**, run the resolved `workflow.on_complete` instruction, if any,
then invoke `help` to recommend sprint planning for the next horizon.
