from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT NOT NULL,
            name TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        marks = request.form["marks"]
        cur.execute("INSERT INTO students (roll, name, marks) VALUES (?, ?, ?)", (roll, name, marks))
        conn.commit()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return render_template("index.html", students=students)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
