from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from make_database import query_db, insert_db, init_db

app = Flask(__name__)

# Initialize the database
with app.app_context():
    init_db()

# Route to display a user's profile and their tasks
@app.route('/profile/<username>')
def profile(username):
    # Get user information
    user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
    
    if user is None:
        return "User not found!", None

    # Get tasks for the user
    tasks = query_db('SELECT * FROM tasks WHERE user_id = ?', [user[0]])
    
    return render_template('profile.html', user=user, tasks=tasks)

# Route to add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    user_id = request.form['user_id']
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    due_date = request.form['due_date']

    insert_db('''
        INSERT INTO tasks (user_id, title, description, priority, due_date) 
        VALUES (?, ?, ?, ?, ?)''', 
        [user_id, title, description, priority, due_date])

    return redirect(url_for('profile', username=request.form['username']))

# Route to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        insert_db('INSERT INTO users (username, email) VALUES (?, ?)', 
                  [username, email])

        return redirect(url_for('profile', username=username))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)