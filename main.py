from flask import Flask, render_template, request, redirect, session, url_for
import os
import business_logic

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    
    # Fallback if we have logged_in but no user_id (migration from old session)
    if not user_id:
         session.clear()
         return redirect(url_for('login'))

    user_tasks = business_logic.get_user_tasks(user_id)
    return render_template('index.html', tasks=user_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = business_logic.validate_login(username, password)
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user['id'] # Storing ID is much better!
            return redirect(url_for('index'))
        else:
            error = 'INVALID_CREDENTIALS'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = business_logic.register_user(username, password)
        if success:
            return redirect(url_for('login'))
        else:
            # Pass error message to template (assumes register.html can handle it or just raw return)
            # Original code returned string. Retaining that behavior or improving?
            # Original: return "Username taken."
            return message
            
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_task():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    name = request.form.get('task_name')
    urgency = request.form.get('urgency')
    importance = request.form.get('importance')

    success, msg = business_logic.add_new_task(user_id, name, urgency, importance)
    if not success:
        return f"Error: {msg}", 500
    
    return redirect(url_for('index'))

@app.route('/complete/<task_id>')
def complete_task(task_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    business_logic.mark_task_complete(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    business_logic.remove_task(task_id)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)