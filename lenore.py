import subprocess
import sys
import os

os.system("python.exe -m pip install --upgrade pip")
for package in ["terminaltexteffects", "python-socketio", "getmac"]:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from terminaltexteffects.effects.effect_binarypath import BinaryPath
from terminaltexteffects.effects.effect_expand import Expand
import socketio
import logging
import socket
import getmac

LOGO_TEXT = """                     
  `7MMF'                                                                              
    MM                                                                  ,;//'         
    MM         .gP"Ya  `7MMpMMMb.   ,pW"Wq.  `7Mb,od8  .gP"Ya        ,;//'    pd""b.  
    MM        ,M'   Yb   MM    MM  6W'   `Wb   MM' "' ,M'   Yb     ,//'      (O)  `8b 
    MM      , 8M""""""   MM    MM  8M     M8   MM     8M""""""     `\\.           ,89 
    MM     ,M YM.    ,   MM    MM  YA.   ,A9   MM     YM.    ,        `\\:.     ""Yb. 
  .JMMmmmmMMM  `Mbmmd' .JMML  JMML. `Ybmd9'  .JMML.    `Mbmmd'           `\\.      88 
                                                                           (O)  .M' 
                                                                            bmmmd'  

  ┌── by: Matheus Barros ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                                                                                                                             │
  │ 1 -- | LOGIN                                                                                                                                                                                                │
  │ 2 -- | REGISTER                                                                                                                                                                                             │
  │ 3 -- | QUIT                                                                                                                                                                                                 │
  │                                                                                                                                                                                                             │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""
WELCOME_TEXT = """

 __ __ __      ______      __          ______      ______      ___ __ __      ______      
/_//_//_/\    /_____/\    /_/\        /_____/\    /_____/\    /__//_//_/\    /_____/\     
\:\\:\\:\ \   \::::_\/_   \:\ \       \:::__\/    \:::_ \ \   \::\| \| \ \   \::::_\/_    
 \:\\:\\:\ \   \:\/___/\   \:\ \       \:\ \  __   \:\ \ \ \   \:.      \ \   \:\/___/\   
  \:\\:\\:\ \   \::___\/_   \:\ \____   \:\ \/_/\   \:\ \ \ \   \:.\-/\  \ \   \::___\/_  
   \:\\:\\:\ \   \:\____/\   \:\/___/\   \:\_\ \ \   \:\_\ \ \   \. \  \  \ \   \:\____/\ 
    \_______\/    \_____\/    \_____\/    \_____\/    \_____\/    \__\/ \__\/    \_____\/ 

┌── THE RULES ──────────────────────────────────────────────────────────────────────────┐
│                                                                                       │
│ * this chat was created with the intention of give you the oportunity to share        │
│   your ideas and talk about random stuff.                                             │
│ * does not mean that you will not be punished if you disrespect the order of our      │   
│   members.                                                                            │   
│ * the creator of the chat liked the project so much that he decided to choose two     │
│   awesome administrators to rule the chat                                             │
│                                                                                       │
│         ┌───────────────────────────────────────────────────────────────────┐         │
│         │                              ADMINS:                              │         │    
│         │ 1. Matheus Henrique [br] @troy                                    │         │   
│         │ 2. João Nunes [pt] @cogito                                        │         │
│         │ 3. Martim Gabriel [pt] @mafanhoto                                 │         │
│         └───────────────────────────────────────────────────────────────────┘         │
│                                                                                       │
│ 1 -- | DO NOT FLOOD                                                                   │
│ 2 -- | DO NOT BULLY                                                                   │
│ 3 -- | DO NOT SPAM                                                                    │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
"""

IP_ADDRESS = ""
MAC_ADDRESS = ""

LOGO = BinaryPath(LOGO_TEXT)
LOGO.terminal_config.canvas_width = -1
LOGO.terminal_config.canvas_height = -1
LOGO.effect_config.movement_speed = 2

WELCOME = Expand(WELCOME_TEXT)
HOSTNAME = socket.gethostname()

username = ""
password = ""
client = None
events = None
is_logged_in = False

# ── PRESTUFF ─────────────────────────────────────────────────────────
class ClientEvents:
    def __init__(self, client):
        self.client = client
        client.on("connect", self.connect)
        client.on("disconnect", self.disconnect)
        client.on("new_message", self.new_message)

    def connect(self):
        print("[s] : connected to the server")

    def disconnect(self):
        print("[s] : disconnected from the server")

    def new_message(self, data):
        if is_logged_in:
            print(f"@{data['username']} | {data['content']}")

    def load_messages(self):
        return self.client.call("load_messages")
class Utils:
    @staticmethod
    def load_messages(history):
        for message in history:
            print(f"@{message['username']} | {message['content']}")

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def my_prompt(prompt=""):
        content = input(prompt)
        sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        return content

    @staticmethod
    def get_ip():
        return socket.gethostbyname(HOSTNAME)

    @staticmethod
    def get_mac():
        return getmac.get_mac_address()

    @staticmethod
    def register():
        global is_logged_in, username, username_checking

        username_checking = input("username: ")
        password_checking = input("password: ")

        if username_checking == "/exit":
            LOGO.effect_config.movement_speed = 500
            main()
            return

        result = client.call("register", {
            "username": username_checking,
            "password": password_checking,
            "ip_address": IP_ADDRESS,
            "mac_address": MAC_ADDRESS
        })

        if result["okay"]:
            print("[s] : user created !")
            input("((press enter))")
            is_logged_in = True
            username = username_checking
            LOGO.effect_config.movement_speed = 10
        else:
            print(f"[s] : {result['error']}")
            Utils.register()
    
    """def ban():
        global username, IP_ADDRESS, MAC_ADDRESS
        
        result = client.call("ban", {
            "username" : username,
            "ip_address" : IP_ADRESS,
            "mac_address" : MAC_ADDRESS
        })
        
        if result["okay"]:
            print("[s] you got banned !")
            client.emit("msg", {
                "username" : "system",
                "content" : "a user got banned !"
            })"""
    
    @staticmethod
    def login():
        global is_logged_in, username_checking, username

        username_checking = input("username: ")

        if username_checking == "/exit":
            LOGO.effect_config.movement_speed = 500
            main()
            return

        password_checking = input("password: ")

        result = client.call("login", {
            "username": username_checking,
            "password": password_checking
        })

        if result["okay"]:
            is_logged_in = True
            username = username_checking
            print("[s] : welcome!")
            LOGO.effect_config.movement_speed = 10
        else:
            print("[s] : invalid username or password")
            Utils.login()
class Init:
    @staticmethod
    def start():
        global client, events, IP_ADDRESS, MAC_ADDRESS

        Utils.clear_screen()
        logging.disable(logging.CRITICAL)

        cloudflare_code = input("[s] recent code : ").strip()
        s = f"https://{cloudflare_code}.trycloudflare.com"

        client = socketio.Client(logger=False, engineio_logger=False)
        events = ClientEvents(client)

        try:
            client.connect(s, wait_timeout=15)
        except socketio.exceptions.ConnectionError as exc:
            print(f"[s] : connection failed: {exc}")
            return False

        IP_ADDRESS = Utils.get_ip()
        MAC_ADDRESS = Utils.get_mac()

        return True

# ── MAIN ─────────────────────────────────────────────────────────────
def main():
    global is_logged_in

    if not Init.start():
        return

    if not is_logged_in:
        with LOGO.terminal_output() as terminal:
            for frame in LOGO:
                terminal.print(frame)

        LRD = input("#: ")
        Utils.clear_screen()

        if LRD == "1":
            Utils.login()
        elif LRD == "2":
            Utils.register()
        else:
            print("[s] : see you latter !")
            client.disconnect()
            return

    if not is_logged_in:
        return

    with WELCOME.terminal_output() as terminal:
        for frame in WELCOME:
            terminal.print(frame)

    history = events.load_messages()
    Utils.load_messages(history)

    while True:
        try:
            content = Utils.my_prompt()
        except (EOFError, KeyboardInterrupt):
            break

        if content == "/exit":
            is_logged_in = False
            break

        if not content.strip():
            continue

        client.emit("msg", {
            "username": username,
            "content": content
        })

    if client.connected:
        client.disconnect()
if __name__ == "__main__":
    main()
