# Record Implementation Evidence

Shared sub-step for recording that effectful implementation actually
happened. Called after the Commit step, once a commit exists.

## Preconditions

Skip entirely when no commit was created in this workflow run (VCS
unavailable, or the tree was already clean). Skip when `slice_id` or
`run_dir` is unset.

## Instructions

1. Get the commit hash and subject with `git log -1 --format='%H %s'`, and
   the changed-file list with `git show --stat --format= HEAD`.
2. Append one entry to `{run_dir}/04-implementation/{slice_id}.md` (create
   the file with a `# Implementation evidence: {slice_id}` heading first if
   it does not exist yet — this file accumulates one entry per commit made
   against this slice, oldest first):

   ```markdown
   ## {commit_hash} — {commit_subject}

   Files changed:
   - {path}
   - {path}

   Verification: {the acceptance/verification commands run for this
   commit and their result, in one line}
   ```

3. Register the file: it does not need re-registration on later entries
   once its path is already `current`.

   ```text
   uv run _agent-workflows/scripts/run_state.py add-artifact \
     --run-dir "{run_dir}" --path "04-implementation/{slice_id}.md" \
     --type "implementation-evidence" --status "current"
   ```
