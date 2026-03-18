# Django Notes App

A simple note-taking web application built with Django and SQLite.

## Features

- Create, read, update, and delete notes
- Persistent storage using SQLite
- Basic input validation and error handling
- Responsive web interface with modern design
- Flash messages for user feedback
- Django admin interface for advanced management

## Tech Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Django templates
- **ORM**: Django ORM

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd week8/django_notes
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

4. Apply migrations and create the database:
   ```bash
   python manage.py migrate
   ```

## Running the Application

```bash
python manage.py runserver
```

The application will start running on `http://localhost:8000`.

## Creating an Admin User

For advanced management through the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user, then access the admin interface at `http://localhost:8000/admin`.

## Usage

- **View Notes**: Visit the homepage to see all existing notes
- **Create Note**: Click "Add Note" button to create a new note
- **Edit Note**: Click "Edit" button on any note to update it
- **Delete Note**: Click "Delete" button on any note to remove it
- **Admin Interface**: Access `/admin` to manage notes with advanced features

## Database

The application uses SQLite for storage. The database file `db.sqlite3` will be automatically created in the project directory when migrations are applied.

## Project Structure

```
django_notes/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── django_notes/          # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project URLs
│   └── wsgi.py            # WSGI configuration
└── notes/                 # Notes app
    ├── __init__.py
    ├── admin.py           # Admin configuration
    ├── apps.py            # App configuration
    ├── models.py          # Data models
    ├── forms.py           # Form definitions
    ├── views.py           # Views and business logic
    ├── urls.py            # App URLs
    └── templates/         # HTML templates
        └── notes/
            ├── base.html  # Base template with common elements
            ├── index.html # Homepage with notes list
            ├── form.html  # Create/update note form
            └── delete.html # Delete confirmation page
```

## Default Configuration

The application comes with a default configuration including:
- SQLite database with automatic migration support
- Default Django security settings
- Simple authentication system
- Static file serving for development

## Development Features

- Automatic database migration
- Built-in admin interface
- Development server with hot reloading
- Comprehensive error handling
- Debug toolbar support (if installed)

## Production Deployment

For production deployment:
1. Use a production-grade database (PostgreSQL or MySQL)
2. Configure static file storage
3. Enable HTTPS
4. Set debug mode to False
5. Use a WSGI server like Gunicorn
