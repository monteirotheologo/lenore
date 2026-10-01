from flask import Flask
from flask_socketio import SocketIO
from colorama import Fore, Style
import os

IP="0.0.0.0"
PORT=5555

app = Flask(__name__)
server = SocketIO(app)

colorAdmin = Fore.RED + Style.BRIGHT
colorUserLinux = Fore.GREEN + Style.BRIGHT
colorUserWindows = Fore.BLUE + Style.BRIGHT
colorUserOtherOs = Fore.CYAN + Style.BRIGHT
r = Style.RESET_ALL

@server.on("msg")
def msg(user, msg_content):
    if os.name == "nt":
        text = f"{colorUserWindows}@{user}{r} | {msg_content}"
    elif os.name == "posix":
        text = f"{colorUserLinux}@{user}{r} | {msg_content}"
    else:
        text = f"{colorUserOtherOs}@{user}{r} | {msg_content}"
    print(text)

import sqlite3

@staticmethod
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        grade INTEGER NOT NULL
    )   
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id_messages INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id_user)
    )
    """)

    conn.commit()
    conn.close()

@staticmethod
def if_user_exists(username):
    conn = sqlite3.connect("database.db")

    result = conn.execute("""
    SELECT id_user FROM users WHERE username = ?
    """, (username,)).fetchone()

    conn.close()
    return result is not None

@staticmethod
def if_password_match(username, password):
    conn = sqlite3.connect("database.db")

    result = conn.execute("""
    SELECT id_user FROM users WHERE username = ? AND password = ?
    """, (username, password,)).fetchone()

    conn.close()
    return result is not None

@staticmethod
def create_user(username, password):
    conn = sqlite3.connect("database.db")
    conn.execute("""
    INSERT INTO users (username, password, grade) VALUES (?, ?, 0)
    """, (username, password))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    server.run(app, host=IP, port=PORT, allow_unsafe_werkzeug=True)