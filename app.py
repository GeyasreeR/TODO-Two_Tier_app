from flask import Flask, request, jsonify, render_template
import sqlite3


app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("todos.db")
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER DEFAULT 0)")
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            conn = sqlite3.connect("todos.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
            conn.close()
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return render_template("index.html", todos=todos)


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    completed = request.json.get("completed")
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = ? WHERE id = ?", (1 if completed else 0, todo_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return jsonify(todos)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

