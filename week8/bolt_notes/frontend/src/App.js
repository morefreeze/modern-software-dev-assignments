import React, { useState, useEffect } from 'react';
import NoteList from './components/NoteList';
import NoteForm from './components/NoteForm';
import { getNotes, createNote, updateNote, deleteNote } from './services/api';

function App() {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [flashMessage, setFlashMessage] = useState(null);

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const data = await getNotes();
      setNotes(data);
    } catch (error) {
      showFlash('Failed to fetch notes', 'error');
    }
  };

  const showFlash = (message, type) => {
    setFlashMessage({ message, type });
    setTimeout(() => {
      setFlashMessage(null);
    }, 3000);
  };

  const handleCreateNote = async (noteData) => {
    try {
      const newNote = await createNote(noteData);
      setNotes([newNote, ...notes]);
      setIsFormVisible(false);
      showFlash('Note created successfully', 'success');
    } catch (error) {
      showFlash('Failed to create note', 'error');
    }
  };

  const handleEditNote = async (noteData) => {
    try {
      const updatedNote = await updateNote(selectedNote.id, noteData);
      setNotes(notes.map(note => 
        note.id === selectedNote.id ? updatedNote : note
      ));
      setSelectedNote(null);
      setIsFormVisible(false);
      showFlash('Note updated successfully', 'success');
    } catch (error) {
      showFlash('Failed to update note', 'error');
    }
  };

  const handleDeleteNote = async (id) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await deleteNote(id);
        setNotes(notes.filter(note => note.id !== id));
        showFlash('Note deleted successfully', 'success');
      } catch (error) {
        showFlash('Failed to delete note', 'error');
      }
    }
  };

  const handleStartEdit = (note) => {
    setSelectedNote(note);
    setIsFormVisible(true);
  };

  const handleCancelForm = () => {
    setSelectedNote(null);
    setIsFormVisible(false);
  };

  return (
    <div className="container">
      <header>
        <h1>Bolt Notes</h1>
        {!isFormVisible && (
          <button 
            className="btn btn-primary"
            onClick={() => setIsFormVisible(true)}
          >
            Add Note
          </button>
        )}
      </header>

      {flashMessage && (
        <div className={`flash ${flashMessage.type}`}>
          {flashMessage.message}
        </div>
      )}

      {isFormVisible ? (
        <NoteForm
          note={selectedNote}
          onSubmit={selectedNote ? handleEditNote : handleCreateNote}
          onCancel={handleCancelForm}
        />
      ) : (
        <NoteList
          notes={notes}
          onEdit={handleStartEdit}
          onDelete={handleDeleteNote}
        />
      )}
    </div>
  );
}

export default App;
