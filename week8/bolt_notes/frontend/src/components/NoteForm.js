import React, { useState, useEffect } from 'react';

const NoteForm = ({ note, onSubmit, onCancel }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content);
    } else {
      setTitle('');
      setContent('');
    }
  }, [note]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      alert('Title is required');
      return;
    }

    onSubmit({
      title: title.trim(),
      content: content.trim()
    });
  };

  const handleCancel = () => {
    if (title || content) {
      if (window.confirm('Are you sure you want to cancel? Unsaved changes will be lost.')) {
        onCancel();
      }
    } else {
      onCancel();
    }
  };

  return (
    <div>
      <h2>{note ? 'Edit Note' : 'Create New Note'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            className="form-control"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Note title..."
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            className="form-control"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Note content..."
            rows="5"
          />
        </div>
        <div className="btn-group">
          <button type="submit" className="btn btn-primary">
            {note ? 'Update Note' : 'Create Note'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleCancel}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default NoteForm;
