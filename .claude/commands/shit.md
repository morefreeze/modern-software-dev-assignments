# /shit — Output Knowledge & Clean Workspace

Synthesize everything absorbed from the codebase into actionable outputs, then clean up the workspace.

## Steps

### Phase 1: Output Knowledge

1. **Generate a master status report** — write to `STATUS.md` at the repo root:
   - Completion status of each week (complete / partial / incomplete)
   - What's missing per week (code, tests, writeup fields, etc.)
   - Recommended next actions, prioritized by impact

2. **Fill any remaining writeup TODOs** — for each week that has a `writeup.md` with TODO fields:
   - Check if corresponding `plan.md` or source code has the information needed
   - Fill in what can be inferred from the code and plan
   - Leave only genuinely unknown fields (Name, SUNet ID, PR links) as TODO

3. **Generate missing READMEs** — for any week directory missing a `README.md`, generate one from the source code covering:
   - What the project does
   - Setup instructions
   - How to run tests
   - Key files and their purpose

### Phase 2: Clean Workspace

4. **Remove temporary/debug files**:
   - Delete any `*.pyc` files outside of `__pycache__` directories
   - Delete any `.DS_Store` files
   - Delete any `tmp_*` or `debug_*` files

5. **Identify stale worktrees** — list any git worktrees that are no longer needed (check with `git worktree list`) and report them for manual cleanup (do NOT delete worktrees automatically).

6. **Report what was done** — output a summary of all files created, modified, and cleaned.

### Output

End with a clean summary:
```
OUTPUTS GENERATED:
  - STATUS.md (created)
  - week_/writeup.md (N fields filled)
  - week_/README.md (created)

CLEANUP:
  - N temporary files removed
  - Worktrees to review: [list]
```
