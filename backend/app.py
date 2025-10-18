from flask import Flask, request, redirect, send_from_directory, session
import sqlite3
import os

# Configuración de Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.secret_key = "mi_clave_secreta"  # Necesario para manejar sesiones

DB_NAME = 'users.db'

# Inicializar la base de datos y crear usuario demo
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
    # Usuario demo: admin / 1234
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?,?)", ("admin", "1234"))
    conn.commit()
    conn.close()

init_db()

# Ruta login (POST)
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
        session['user'] = username  # Guardar usuario en sesión
        return redirect("/main.html")
    else:
        return "Usuario o contraseña incorrectos"

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/login.html")

# Servir main.html solo si está logueado
@app.route('/main.html')
def main_page():
    if 'user' in session:
        return app.send_static_file('main.html')
    else:
        return redirect('/login.html')

# Servir cualquier archivo estático desde frontend/
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)