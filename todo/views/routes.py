from datetime import datetime
from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo

api = Blueprint("api", __name__, url_prefix="/api/v1")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@api.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])


@api.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify(todo.to_dict())


@api.route("/todos", methods=["POST"])
def create_todo():
    data = request.json

    todo = Todo(
        title=data.get("title"),
        description=data.get("description"),
        completed=data.get("completed", False),
    )

    if "deadline_at" in data and data["deadline_at"]:
        todo.deadline_at = datetime.fromisoformat(data["deadline_at"])

    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@api.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    data = request.json

    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    todo.completed = data.get("completed", todo.completed)

    if "deadline_at" in data:
        value = data["deadline_at"]
        todo.deadline_at = datetime.fromisoformat(value) if value else None

    db.session.commit()

    return jsonify(todo.to_dict())


@api.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({}), 200

    db.session.delete(todo)
    db.session.commit()

    return jsonify(todo.to_dict())
