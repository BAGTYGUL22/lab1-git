from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем базу данных SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"

db = SQLAlchemy(app)


# Создаем модель заметки
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)


# Создаем таблицы в базе данных
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"message": "Notes API is working!"}


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()

    result = []

    for note in notes:
        result.append({
            "id": note.id,
            "title": note.title,
            "content": note.content
        })

    return result


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Invalid JSON"}, 400

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not title.strip():
        return {"error": "Title is required"}, 400

    if not isinstance(content, str) or not content.strip():
        return {"error": "Content is required"}, 400

    new_note = Note(title=title, content=content)

    db.session.add(new_note)
    db.session.commit()

    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content
    }, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = db.session.get(Note, note_id)

    if note is None:
        return {"error": "Note not found"}, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Invalid JSON"}, 400

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not title.strip():
        return {"error": "Title is required"}, 400

    if not isinstance(content, str) or not content.strip():
        return {"error": "Content is required"}, 400

    note.title = title
    note.content = content

    db.session.commit()

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content
    }


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = db.session.get(Note, note_id)

    if note is None:
        return {"error": "Note not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted successfully"}


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = db.session.get(Note, note_id)

    if note is None:
        return {"error": "Note not found"}, 404

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content
    }


if __name__ == "__main__":
    app.run(debug=True)
