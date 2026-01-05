from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- DATABASE LAYER SETUP ---
def init_db():
    conn = sqlite3.connect('timeframe.db')
    cursor = conn.cursor()
    # User Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    # Tasks Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       user_id INTEGER, 
                       name TEXT, 
                       category TEXT, 
                       status TEXT DEFAULT 'pending',
                       FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('timeframe.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user_id = cursor.fetchone()[0]
    
    cursor.execute('SELECT id, name, category, status FROM tasks WHERE user_id = ?', (user_id,))
    user_tasks = [dict(id=row[0], name=row[1], category=row[2], status=row[3]) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('index.html', tasks=user_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('timeframe.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'INVALID_CREDENTIALS'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('timeframe.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            return "Username taken."
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_task():
    if not session.get('logged_in'): return redirect(url_for('login'))
    name = request.form.get('task_name')
    urgency = request.form.get('urgency')
    importance = request.form.get('importance')

    if urgency == 'urgent' and importance == 'important': cat = 'Q1'
    elif urgency == 'not_urgent' and importance == 'important': cat = 'Q2'
    elif urgency == 'urgent' and importance == 'not_important': cat = 'Q3'
    else: cat = 'Q4'

    conn = sqlite3.connect('timeframe.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    u_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO tasks (user_id, name, category) VALUES (?, ?, ?)', (u_id, name, cat))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('timeframe.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('timeframe.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # host='0.0.0.0' tells Flask to listen to external requests
    app.run(debug=True, host='0.0.0.0', port=5000)