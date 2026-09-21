import socket 		# biblioteca para criar o server, receber clientes e deixar online
import threading 	# biblioteca para que muitos users possam receber mensagens em tempo real
import openai 		# biblioteca que vai integrar uma IA ao chat
import sqlite3		# biblioteca para guardar as mensagens e os usuários
import colorama     # autoexplicativo
import hashlib      # biblioteca para criptografar a senha

# LET'S GOOOOOO !!!!!!

# --- Configuração da database: ------------------------------------------------------------------

class DB:
    @staticmethod
    def CreateDB():
        try:
            conn = sqlite3.connect("lenore_database.db")
            try:
                conn.executescript("""
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS users (
                    userid integer primary key autoincrement,
                    username text not null,
                    userpass text not null,
                    userlevel int not null
                );
                CREATE TABLE IF NOT EXISTS messages (
                    messageid integer primary key autoincrement,
                    userid integer not null,
                    FOREIGN KEY (userid) REFERENCES users(userid),
                    userlevel int not null,
                    FOREIGN KEY (userlevel) REFERENCES users(userlevel),
                    messagecontent text not null
                )
                """)
                conn.commit()
            finally:
                conn.close()
        except sqlite3.Error as e:
            print(f"[STATUS] : {e}")

    @staticmethod
    def EncryptedPassword(userpass: str) -> str:
        return hashlib.sha256(userpass.encode("utf-8")).hexdigest()

    @staticmethod
    def CreateUser(username: str, userpass: str, userlevel: int):
        hashed_password = DB.EncryptedPassword(userpass)
        conn = sqlite3.connect("lenore_database.db")
        try:
            conn.execute(
                "INSERT INTO users(username, userpass, userlevel) VALUES (?, ?, ?)",
                (username, hashed_password, userlevel)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def CheckLogin(username: str, try_password: str) -> bool:
        conn = sqlite3.connect("lenore_database.db")
        try:
            cursor = conn.execute(
                "SELECT userpass FROM users WHERE username = ?",
                (username,)
            )
            eye = cursor.fetchone()

            if eye is None:
                return False

            saved_hash = eye[0]
            tried_hash = DB.EncryptedPassword(try_password)

            return saved_hash == tried_hash
        finally:
            conn.close()

    @staticmethod
    def SendMessage(userid: int, messagecontent: str, userlevel: int):
        conn = sqlite3.connect("lenore_database.db")
        try: 
            conn.execute(
                "INSERT INTO messages(userid, messagecontent, userlevel) VALUES (?, ?, ?)", # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                (userid, messagecontent, userlevel)
            )
            conn.commit()
        finally:
            conn.close()
# --- Main: ------------------------------------------------------------------

class Main:
    @staticmethod
    def Main():
        print("Welcome to Lenore Chat!")
        print("Please enter your username:")
        username = input()
        print("Please enter your password:")
        password = input()
