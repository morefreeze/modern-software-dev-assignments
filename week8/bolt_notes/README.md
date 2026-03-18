# Bolt Notes App (AI-Generated)

A modern note-taking web application built with React frontend and Express backend, created in the style of bolt.new AI-generated apps.

## Features

- Create, read, update, and delete notes
- Persistent storage using SQLite
- Responsive React interface with real-time updates
- Basic input validation and error handling
- Flash messages for user feedback
- RESTful API backend

## Tech Stack

- **Backend**: Node.js + Express
- **Database**: SQLite3
- **Frontend**: React 18
- **HTTP Client**: Axios
- **Styling**: Custom CSS with modern design

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd week8/bolt_notes
   ```

### Backend Setup

2. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   npm install
   ```

### Frontend Setup

3. Navigate to the frontend directory and install dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Application

### Start the Backend

```bash
cd backend
npm start
```

The backend server will run on `http://localhost:5000`.

### Start the Frontend

Open a new terminal window:

```bash
cd frontend
npm start
```

The frontend development server will run on `http://localhost:3000`.

## Usage

- **View Notes**: The homepage displays all notes in reverse chronological order
- **Create Note**: Click "Add Note" button to create a new note
- **Edit Note**: Click "Edit" button on any note to update it
- **Delete Note**: Click "Delete" button on any note to remove it (confirmation required)

## Database

The application uses SQLite for storage. The database file `notes.db` will be automatically created in the backend directory when the server starts for the first time.

## Project Structure

```
bolt_notes/
├── backend/
│   ├── package.json        # Backend dependencies
│   ├── server.js           # Main backend server
│   └── notes.db            # SQLite database (created on first run)
└── frontend/
    ├── public/
    │   └── index.html      # HTML entry point
    ├── src/
    │   ├── components/
    │   │   ├── NoteList.js # Note list component
    │   │   └── NoteForm.js # Note form component
    │   ├── services/
    │   │   └── api.js      # API service layer
    │   ├── App.js          # Main App component
    │   ├── index.js        # React entry point
    │   └── index.css       # Global styles
    └── package.json        # Frontend dependencies
```

## API Endpoints

- `GET /api/notes` - Retrieve all notes
- `POST /api/notes` - Create a new note
- `PUT /api/notes/:id` - Update an existing note
- `DELETE /api/notes/:id` - Delete a note

## AI Generation Style Notes

This application was created following the patterns of AI-generated apps like bolt.new, with:

- Clean, modern UI with smooth interactions
- Responsive design
- Intuitive user flow
- Automatic error handling
- Real-time feedback
