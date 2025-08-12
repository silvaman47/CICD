from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

# Database setup
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('todos.db')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
                );'''
        conn.execute(sql)
    except Error as e:
        print(e)

# Initialize DB
conn = create_connection()
if conn:
    create_table(conn)
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = create_connection()
    if request.method == 'POST':
        task = request.form['task']
        if task:
            sql = '''INSERT INTO todos (task, completed) VALUES (?, 0)'''
            cur = conn.cursor()
            cur.execute(sql, (task,))
            conn.commit()
        return redirect(url_for('index'))

    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    conn = create_connection()
    sql = '''UPDATE todos SET completed = 1 WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = create_connection()
    sql = '''DELETE FROM todos WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)