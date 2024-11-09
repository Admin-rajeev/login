from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

USER_FILE = "users.txt"


def load_users():
    """Load users from the file into a dictionary."""
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                users[username] = password
    return users


def save_user(username, password):
    """Save a new user to the file."""
    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")


@app.route('/')
def home():
    return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists!", "warning")
        else:
            save_user(username, password)
            flash("Registration successful! Please log in.", "success")
            return redirect("https://www.instagram.com/p/CGh4a0iASGS/?utm_source=ig_web_button_share_sheet&igsh=MzRlODBiNWFlZA==")
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
