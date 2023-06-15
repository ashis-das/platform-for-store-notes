from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)
# Create a SQLite database connection
conn = sqlite3.connect('notes.db')
c = conn.cursor()
# Create the notes table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS notes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              note_type TEXT,
              note_content TEXT)''')
conn.commit()
# API endpoint to create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    user_id = data['user_id']
    note_type = data['note_type']
    note_content = data['note_content']
    # Insert the note into the database
    c.execute("INSERT INTO notes (user_id, note_type, note_content) VALUES (?, ?, ?)",
              (user_id, note_type, note_content))
    conn.commit()
    return jsonify({'message': 'Note created successfully'})
# API endpoint to retrieve all notes
@app.route('/notes', methods=['GET'])
def get_all_notes():
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    # Convert the notes to a list of dictionaries
    notes_list = [{'id': note[0], 'user_id': note[1], 'note_type': note[2], 'note_content': note[3]} for note in notes]
    return jsonify(notes_list)
# API endpoint to retrieve notes for a specific user
@app.route('/notes/user/<user_id>', methods=['GET'])
def get_user_notes(user_id):
    c.execute("SELECT * FROM notes WHERE user_id=?", (user_id,))
    user_notes = c.fetchall()
    # Convert the user's notes to a list of dictionaries
    user_notes_list = [{'id': note[0], 'user_id': note[1], 'note_type': note[2], 'note_content': note[3]} for note in user_notes]
    return jsonify(user_notes_list)
if __name__ == '__main__':
    app.run(debug=True)
