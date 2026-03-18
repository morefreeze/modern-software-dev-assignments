import React from 'react';

const NoteList = ({ notes, onEdit, onDelete }) => {
  if (notes.length === 0) {
    return (
      <div className="empty-state">
        <p>No notes yet. Click "Add Note" to create your first note.</p>
      </div>
    );
  }

  return (
    <div className="notes-grid">
      {notes.map(note => (
        <div key={note.id} className="note-card">
          <div className="note-header">
            <h3>{note.title}</h3>
            <div className="note-actions">
              <button
                className="btn btn-sm btn-secondary"
                onClick={() => onEdit(note)}
              >
                Edit
              </button>
              <button
                className="btn btn-sm btn-danger"
                onClick={() => onDelete(note.id)}
              >
                Delete
              </button>
            </div>
          </div>
          <p className="note-content">
            {note.content.length > 150 
              ? `${note.content.substring(0, 150)}...` 
              : note.content}
          </p>
          <small className="note-date">
            {new Date(note.createdAt).toLocaleString()}
          </small>
        </div>
      ))}
    </div>
  );
};

export default NoteList;
