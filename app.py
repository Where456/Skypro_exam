from marshmallow import Schema, fields
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_pyfile("default_config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)

db = SQLAlchemy(app)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(255))
    data = db.Column(db.String(255))
    name = db.Column(db.String(255))
    office_number = db.Column(db.String(255))


class ScheduleSchema(Schema):
    id = fields.Integer(dump_only=True)
    course_title = fields.String(required=True, max_length=255)
    data = db.Column(db.String(255))
    name = db.Column(db.String(255))
    office_number = db.Column(db.String(255))


with app.app_context():
    db.create_all()


@app.route("/")
def get_schedule():
    """
        Получает все заметки из базы данных и возвращает их в формате JSON.

        Returns:
            JSON: Список заметок в формате JSON.
    """
    data = Schedule.query.all()
    schedule_data = []
    for d in data:
        schedule_data.append({
            'id': d.id,
            'course_title': d.course_title,
            'data': d.data,
            'name': d.name,
            'office_number': d.office_number
        })
    return jsonify(schedule_data)


@app.route("/add", methods=["POST"])
def add_schedule():
    """
        Добавляет новую информацию в базу данных.

        Returns:
            JSON: Результат операции добавления.
    """
    schedule_data = request.json
    if not schedule_data or "course_title" not in schedule_data:
        return jsonify({"error": "invalid_request"}), 400

    try:
        schedule = Schedule(
            course_title=schedule_data["course_title"],
            data=schedule_data["data"],
            name=schedule_data["name"],
            office_number=schedule_data["office_number"],
        )
        db.session.add(schedule)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "already_exists"}), 400

    return jsonify({"course_title": schedule.course_title}), 200


@app.route('/delete/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """
        Удаляет заметку из базы данных по указанному идентификатору.

        Args:
            schedule_id (int): Идентификатор заметки.

        Returns:
            str: Результат операции удаления.
    """
    data = Schedule.query.get(schedule_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        return f"Data with ID {schedule_id} has been deleted."
    else:
        return f"Data with ID {schedule_id} does not exist."


@app.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """
        Обновляет заметку в базе данных по указанному идентификатору.

        Args:
            schedule_id (int): Идентификатор заметки.

        Returns:
            str: Результат операции обновления.
    """
    data = Schedule.query.get(schedule_id)
    if data:
        new_course_title = request.json.get('course_title')
        new_data = request.json.get('data')
        new_name = request.json.get('name')
        new_office_number = request.json.get('new_office_number')

        data.course_title = new_course_title if new_course_title else data.course_title
        data.data = new_data if new_data else data.data
        data.name = new_name if new_name else data.name
        data.office_number = new_office_number if new_office_number else data.office_number

        db.session.commit()
        return f"Data with ID {schedule_id} has been updated."
    else:
        return f"Data with ID {schedule_id} does not exist."


if __name__ == "__main__":
    app.run(debug=True)
