# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do.


## Brief findings overview
> Semgrep found **6 blocking issues** across the codebase. Fixed 3 of them: SQL injection via f-string in SQLAlchemy text(), shell injection via `subprocess.run(shell=True)`, and stored XSS via `innerHTML` in the frontend. The remaining 3 issues (wildcard CORS, `eval()`, and `urlopen`) were intentionally accepted — they are debug/demo endpoints or local dev configuration and not part of the production code path. After fixes, re-running Semgrep confirmed findings dropped from 6 to 3.

## Fix #1
a. File and line(s)
> `backend/app/routers/notes.py`, lines 71–79 (the `unsafe_search` function)

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`

c. Brief risk description
> The code built a raw SQL `LIKE` query using an f-string containing user-supplied input directly inside `sqlalchemy.text()`. An attacker can inject SQL metacharacters (e.g., `' OR '1'='1`) to manipulate the query, exfiltrate data, or bypass access controls.

d. Your change (short code diff or explanation, AI coding tool usage)
> Replaced the raw `text()` f-string query with SQLAlchemy ORM operators:
> ```python
> # Before
> sql = text(f"SELECT ... WHERE title LIKE '%{q}%' OR content LIKE '%{q}%' ...")
>
> # After
> stmt = select(Note)
> stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))
> stmt = stmt.order_by(desc(Note.created_at)).limit(50)
> rows = db.execute(stmt.offset(0)).scalars().all()
> ```
> Claude Code was used to identify the exact ORM equivalent and generate the fix.

e. Why this mitigates the issue
> SQLAlchemy's `contains()` operator automatically parameterizes the query — user input is passed as a bind parameter, never interpolated directly into the SQL string. This eliminates the SQL injection vector entirely.

## Fix #2
a. File and line(s)
> `backend/app/routers/notes.py`, lines 108–113 (the `debug_run` function)

b. Rule/category Semgrep flagged
> `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`

c. Brief risk description
> `subprocess.run(cmd, shell=True)` passes the command string through the shell interpreter. If `cmd` contains user-controlled input with shell metacharacters (`;`, `|`, `&`, `$(...)`, etc.), an attacker can chain arbitrary system commands.

d. Your change (short code diff or explanation, AI coding tool usage)
> ```python
> # Before
> completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
>
> # After
> import shlex
> args = shlex.split(cmd)
> completed = subprocess.run(args, shell=False, capture_output=True, text=True)
> ```
> Used Claude Code to suggest the `shlex.split()` + `shell=False` pattern.

e. Why this mitigates the issue
> `shlex.split()` tokenizes the command string into an argument list without invoking the shell. With `shell=False`, the OS `exec()` call receives a list of arguments directly — the shell never interprets the string, so metacharacter injection is impossible.

## Fix #3
a. File and line(s)
> `frontend/app.js`, line 14 (the `loadNotes` rendering loop)

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-document-method.insecure-document-method`

c. Brief risk description
> `li.innerHTML = \`<strong>${n.title}</strong>: ${n.content}\`` inserts user-generated note content directly as HTML. A malicious note whose title or content contains `<script>` tags or event-handler attributes will execute JavaScript in every viewer's browser (stored XSS).

d. Your change (short code diff or explanation, AI coding tool usage)
> ```javascript
> // Before
> li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
>
> // After
> const strong = document.createElement('strong');
> strong.textContent = n.title;
> li.appendChild(strong);
> const colon = document.createTextNode(': ');
> li.appendChild(colon);
> const contentNode = document.createTextNode(n.content);
> li.appendChild(contentNode);
> ```
> Claude Code generated the DOM-based replacement; visually identical output.

e. Why this mitigates the issue
> `textContent` treats the assigned value as plain text — it is HTML-entity-escaped by the browser before rendering. No HTML tags are parsed, so no script can be injected regardless of what the note content contains.