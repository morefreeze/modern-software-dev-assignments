# /eat — Absorb All Knowledge

Scan and deeply understand the entire codebase in the current working directory.

## Steps

1. **Read the project structure**: List all directories and files recursively (excluding `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`).

2. **Read key files**: For each week directory found, read:
   - `assignment.md` — understand the requirements
   - `plan.md` — understand what was implemented and why
   - `writeup.md` — understand the current state of documentation
   - `README.md` — understand setup and usage
   - Core source files (routers, services, models, schemas)
   - Test files

3. **Read project-level context**:
   - Root `CLAUDE.md` (if present)
   - Any `.env.example` or configuration files

4. **Build a mental model**: After reading, summarize what you learned:
   - What each week's assignment covers
   - What is complete vs incomplete
   - Key architectural patterns used across weeks
   - Any cross-week dependencies or shared patterns

5. **Confirm absorption**: Output a concise summary table of all weeks with their completion status and key technologies used.

Do NOT modify any files. This is a read-only knowledge ingestion pass.
