# Week 6 - Semgrep Vulnerability Scanning: Results Summary

## [x] 1. Initial Scan Results

Semgrep found **6 blocking issues** across the codebase:

| # | File | Rule | Severity | Status |
|---|------|------|----------|--------|
| 1 | `backend/app/main.py` | Wildcard CORS `allow_origins=["*"]` | blocking | **Accepted** - intentional for local dev |
| 2 | `backend/app/routers/notes.py` | Raw SQL via `sqlalchemy.text` with f-string (SQL injection) | blocking | ✅ **Fixed** |
| 3 | `backend/app/routers/notes.py` | `eval()` detected (code injection) | blocking | **Accepted** - debug endpoint, intentional for demo |
| 4 | `backend/app/routers/notes.py` | `subprocess.run` with `shell=True` (shell injection) | blocking | ✅ **Fixed** |
| 5 | `backend/app/routers/notes.py` | `urllib.request.urlopen` with dynamic URL (file disclosure) | blocking | **Accepted** - debug endpoint, intentional for demo |
| 6 | `frontend/app.js` | `innerHTML` with user content (XSS) | blocking | ✅ **Fixed** |

## [x] 2. Fixed Issues (Before → After)

### Fix 1: SQL Injection in `notes.py:71-79`

**Issue:** Semgrep rule: `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`

**Risk:** The code used an f-string directly inside `sqlalchemy.text()` to build a LIKE query with user input. This allows SQL injection if the user input contains SQL metacharacters.

**Before:**
```python
sql = text(
    f"""
    SELECT id, title, content, created_at, updated_at
    FROM notes
    WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
    ORDER BY created_at DESC
    LIMIT 50
    """
)
```

**After:**
```python
stmt = select(Note)
stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))
stmt = stmt.order_by(desc(Note.created_at)).limit(50)
rows = db.execute(stmt.offset(0)).scalars().all()
```

**Why this mitigates the issue:**
- Use SQLAlchemy's built-in `contains()` operator instead of raw string interpolation
- SQLAlchemy automatically parameterizes the query
- User input is properly escaped, eliminating SQL injection risk

---

### Fix 2: Shell Injection in `notes.py:108-113`

**Issue:** Semgrep rule: `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`

**Risk:** When `shell=True`, the shell interprets metacharacters like `;`, `|`, `&` allowing command injection if `cmd` contains user input.

**Before:**
```python
completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```

**After:**
```python
import shlex
args = shlex.split(cmd)
completed = subprocess.run(args, shell=False, capture_output=True, text=True)
```

**Why this mitigates:**
- `shlex.split()` properly splits the command into arguments without shell interpretation
- `shell=False` directly executes the binary without going through the shell
- Prevents shell injection even if the command contains user input with shell metacharacters

---

### Fix 3: XSS in `frontend/app.js:14`

**Issue:** Semgrep rule: `javascript.browser.security.insecure-document-method.insecure-document-method`

**Risk:** `innerHTML` parses HTML from user input. If a user creates a note with HTML containing malicious JavaScript, it will execute in the browser of other users (stored XSS).

**Before:**
```javascript
li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
```

**After:**
```javascript
// Use textContent instead of innerHTML to prevent XSS
const strong = document.createElement('strong');
strong.textContent = n.title;
li.appendChild(strong);
const colon = document.createTextNode(': ');
li.appendChild(colon);
const contentNode = document.createTextNode(n.content);
li.appendChild(contentNode);
```

**Why this mitigates:**
- User-generated content is inserted as text, not parsed as HTML
- No HTML interpretation means no risk of executing malicious script from stored XSS
- The visual output is identical (still bolds the title)

## [x] 3. False Positives Analysis

We didn't find any false positives. All findings were genuine security issues:
1. The SQL injection pattern was real - user input directly in SQL string
2. The shell injection was real - `shell=True` with user-controlled command
3. The XSS finding was real - user content in `innerHTML`

## [x] 4. Summary

**Fixed 3 out of 6 blocking issues:**
- [x] SQL injection - fixed by using ORM operators
- [x] Shell injection - fixed by `shlex.split` + `shell=False`
- [x] Reflected XSS - fixed by using `textContent` instead of `innerHTML`

**Remaining 3 are intentional:**
- Wildcard CORS - this is for local development, acceptable
- `eval()` and `urlopen` - these are debug endpoints meant to demonstrate unsafe practices, kept for assignment

## Verification

After fixes, re-running Semgrep confirms the 3 issues are gone:
> ✅ Scan completed successfully. Findings: 3 (was 6)

All 3 required fixes complete.
