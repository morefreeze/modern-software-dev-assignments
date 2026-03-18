const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

const dbPath = path.join(__dirname, 'notes.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
});

app.get('/api/notes', (req, res) => {
    db.all('SELECT * FROM notes ORDER BY createdAt DESC', (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

app.post('/api/notes', (req, res) => {
    const { title, content } = req.body;
    
    if (!title) {
        return res.status(400).json({ error: 'Title is required' });
    }
    
    const stmt = db.prepare('INSERT INTO notes (title, content) VALUES (?, ?)');
    stmt.run([title, content], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ id: this.lastID, title, content });
    });
    stmt.finalize();
});

app.put('/api/notes/:id', (req, res) => {
    const { id } = req.params;
    const { title, content } = req.body;
    
    if (!title) {
        return res.status(400).json({ error: 'Title is required' });
    }
    
    const stmt = db.prepare('UPDATE notes SET title = ?, content = ? WHERE id = ?');
    stmt.run([title, content, id], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (this.changes === 0) {
            return res.status(404).json({ error: 'Note not found' });
        }
        res.json({ id: parseInt(id), title, content });
    });
    stmt.finalize();
});

app.delete('/api/notes/:id', (req, res) => {
    const { id } = req.params;
    
    const stmt = db.prepare('DELETE FROM notes WHERE id = ?');
    stmt.run([id], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (this.changes === 0) {
            return res.status(404).json({ error: 'Note not found' });
        }
        res.json({ message: 'Note deleted successfully' });
    });
    stmt.finalize();
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
