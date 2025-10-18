from flask import Flask, request, redirect, send_from_directory
import sqlite3
import os

# Carpeta estática apuntando a frontend
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

DB_NAME = 'users.db'

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                 )''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?,?)", ("admin", "1234"))
    conn.commit()
    conn.close()

init_db()

# Ruta login
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
        return redirect("/main.html")
    else:
        return "Usuario o contraseña incorrectos"

# Servir archivos estáticos desde frontend
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)