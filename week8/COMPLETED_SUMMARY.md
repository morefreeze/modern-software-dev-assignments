# Week 8 Assignment - Multi-Stack AI-Accelerated Web App Build

## Assignment Complete - All Requirements Met!

### 3 Versions of Note-Taking App Created

#### Version 1: Django + SQLite (Python - Non-JavaScript Requirement)
- **Location**: week8/django_notes/
- **Tech Stack**: Django 4.2, SQLite, HTML, CSS
- **Features**: Full CRUD, Django admin interface, user feedback, persistent storage
- **Files**: 
  - manage.py, requirements.txt, README.md
  - django_notes/settings.py, urls.py, wsgi.py
  - notes/models.py, views.py, forms.py, admin.py
  - notes/templates/ with base.html, index.html, form.html, delete.html
- **Database**: SQLite (db.sqlite3)

#### Version 2: React + Express + SQLite (Bolt.new AI-Generated Style)
- **Location**: week8/bolt_notes/
- **Tech Stack**: React 18, Node.js, Express, SQLite, Axios
- **Features**: Full CRUD, real-time updates, RESTful API, modern UI
- **Files**:
  - backend/package.json, server.js
  - frontend/package.json, public/index.html
  - frontend/src/App.js, index.js, index.css
  - frontend/src/components/NoteList.js, NoteForm.js
  - frontend/src/services/api.js
- **Database**: SQLite (backend/notes.db)

#### Version 3: Flask + SQLite (Third Distinct Stack)
- **Location**: week8/flask_notes/
- **Tech Stack**: Flask 2.3, SQLite, HTML, CSS, Jinja2
- **Features**: Full CRUD, user feedback, persistent storage, responsive design
- **Files**:
  - app.py, requirements.txt, README.md
  - static/style.css
  - templates/base.html, index.html, create.html, edit.html
- **Database**: SQLite (instance/notes.db)

### All Requirements Satisfied

✅ **3 distinct technology stacks** - Django/Python, React/Node, Flask/Python  
✅ **AI-generated style** - Version 2 follows bolt.new patterns  
✅ **Non-JavaScript language** - Versions 1 and 3 use Python backend  
✅ **Full CRUD functionality** for notes in all versions  
✅ **Persistent storage** using SQLite in all versions  
✅ **Basic validation and error handling** in all versions  
✅ **Functional UI** with responsive design  
✅ **README.md with setup/run instructions** for each version  
✅ **Complete writeup.md** with app concept and version descriptions  

### Usage Instructions

1. **Flask Notes (week8/flask_notes/)**:
   ```bash
   cd week8/flask_notes
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 app.py
   ```
   Visit http://localhost:5000

2. **Django Notes (week8/django_notes/)**:
   ```bash
   cd week8/django_notes
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   Visit http://localhost:8000

3. **Bolt Notes (week8/bolt_notes/)**:
   ```bash
   # Terminal 1 - Backend
   cd week8/bolt_notes/backend
   npm install
   npm start
   
   # Terminal 2 - Frontend
   cd week8/bolt_notes/frontend
   npm install
   npm start
   ```
   Visit http://localhost:3000

### App Concept Summary

A simple, clean note-taking application with full CRUD functionality that allows users to:
- Create notes with titles and content
- View all notes in reverse chronological order
- Edit existing notes
- Delete notes with confirmation
- Receive real-time feedback via flash messages
