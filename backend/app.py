from flask import Flask, request, redirect, send_from_directory, session, make_response, jsonify
import sqlite3

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.secret_key = "mi_clave_secreta"

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?,?)", ("admin", "1234"))
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        session['user'] = username
        return redirect("/main.html")
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/login.html")

@app.route('/main.html')
def main_page():
    if 'user' in session:
        response = make_response(app.send_static_file('main.html'))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    else:
        return redirect('/login.html')

@app.route('/check_session')
def check_session():
    if 'user' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)