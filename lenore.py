import socket 		# biblioteca para criar o server, receber clientes e deixar online
import colorama     # autoexplicativo

# LET'S GOOOOOO !!!!!!

# --- Connect: ---------------------------------------------------------------

class Connect:
    @staticmethod
    def login():
        print("Welcome to Lenore Chat!")
        print("Please enter your username:")
        username = input()
        print("Please enter your password:")
        password = input()

# --- Main: ------------------------------------------------------------------

class Main:
    @staticmethod
    def Main():
        Connect.login()
