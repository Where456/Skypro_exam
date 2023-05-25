from marshmallow import Schema, fields
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_pyfile("default_config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=func.now())


class NoteSchema(Schema):
    id = fields.Integer(dump_only=True)
    text = fields.String(required=True, max_length=255)
    date_added = fields.DateTime(dump_only=True)


with app.app_context():
    db.create_all()


@app.route("/")
def get_note():
    """
        Получает все заметки из базы данных и возвращает их в формате JSON.

        Returns:
            JSON: Список заметок в формате JSON.
    """
    notes = Note.query.all()
    note_data = []
    for note in notes:
        note_data.append({
            'id': note.id,
            'text': note.text,
            'date_added': note.date_added
        })
    return jsonify(note_data)


@app.route("/add", methods=["POST"])
def add_note():
    """
        Добавляет новую заметку в базу данных.

        Returns:
            JSON: Результат операции добавления.
    """
    note_data = request.json
    if not note_data or "text" not in note_data:
        return jsonify({"error": "invalid_request"}), 400

    try:
        note = Note(
            text=note_data["text"],
        )
        db.session.add(note)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "already_exists"}), 400

    return jsonify({"text": note.text}), 200


@app.route('/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
        Удаляет заметку из базы данных по указанному идентификатору.

        Args:
            note_id (int): Идентификатор заметки.

        Returns:
            str: Результат операции удаления.
    """
    note = Note.query.get(note_id)

    if note:
        db.session.delete(note)
        db.session.commit()
        return f"Note with ID {note_id} has been deleted."
    else:
        return f"Note with ID {note_id} does not exist."


@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """
        Обновляет заметку в базе данных по указанному идентификатору.

        Args:
            note_id (int): Идентификатор заметки.

        Returns:
            str: Результат операции обновления.
    """
    note = Note.query.get(note_id)
    if note:
        new_title = request.json.get('text')

        note.text = new_title if new_title else note.text

        db.session.commit()
        return f"Note with ID {note_id} has been updated."
    else:
        return f"Note with ID {note_id} does not exist."


if __name__ == "__main__":
    app.run(debug=True)
