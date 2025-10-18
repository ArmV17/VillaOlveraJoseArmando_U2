from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

DB_NAME = 'users.db'

# Inicializar la base de datos si no existe
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                 )''')
    # Crear usuario demo
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

# Servir los archivos estáticos
@app.route('/<path:path>')
def serve_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)