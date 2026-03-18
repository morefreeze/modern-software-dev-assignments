# Flask Notes App

A simple note-taking web application built with Flask and SQLite.

## Features

- Create, read, update, and delete notes
- Persistent storage using SQLite
- Basic input validation and error handling
- Responsive web interface
- Flash messages for user feedback

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Jinja2 templates
- **ORM**: SQLAlchemy

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd week8/flask_notes
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start running on `http://localhost:5000`.

## Usage

- **View Notes**: Visit the homepage to see all existing notes
- **Create Note**: Click "Add Note" button to create a new note
- **Edit Note**: Click "Edit" button on any note to update it
- **Delete Note**: Click "Delete" button on any note to remove it (confirmation required)

## Database

The application uses SQLite for storage. The database file `notes.db` will be automatically created in the project directory when the application runs for the first time.

## Project Structure

```
flask_notes/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html       # Base template with common elements
│   ├── index.html      # Homepage with notes list
│   ├── create.html     # Create new note form
│   └── edit.html       # Edit existing note form
└── static/             # Static files
    └── style.css       # Custom CSS styles
```
