from terminaltexteffects.effects.effect_binarypath import BinaryPath
from terminaltexteffects.effects.effect_expand import Expand
global username
global password
import os

os.system('cls' if os.name == 'nt' else 'clear')

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

  ┌── by: Matheus Barros ─────────────────────────────────────────────────────────────┐
  │                                                                                   │
  │ 1 -- | LOGIN                                                                      │
  │ 2 -- | REGISTER                                                                   │
  │ 3 -- | QUIT                                                                       │
  │                                                                                   │
  └───────────────────────────────────────────────────────────────────────────────────┘
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

WELCOME = Expand(WELCOME_TEXT)

LOGO = BinaryPath(LOGO_TEXT)
LOGO.terminal_config.canvas_width = -1
LOGO.terminal_config.canvas_height = -1
LOGO.effect_config.movement_speed = 2

import os
import sys
import socketio

def my_prompt(prompt=""):
    content = input(prompt)

    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()

    return content

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

s = "https://practitioner-group-cherry-difficulties.trycloudflare.com"

client = socketio.Client(
    logger=True,
    engineio_logger=True,
    reconnection=False
)

client.connect(s)


is_logged_in = False

@client.event
def connect():
    print("[s] : connected to the server")

@client.event
def disconnect():
    print("[s] : disconnected from the server")


@client.on("new_message")
def new_message(data):
    if is_logged_in:
        print(f"@{data['username']} | {data['content']}")

@client.on("load_messages")
def load_messages():
    history = client.call("load_messages")
    for message in history:
        print(f"@{message['username']} | {message['content']}")

def register():
    username_checking = input("username: ")
    password_checking = input("password: ")

    result = client.call("register", {
                "username": username_checking,
                "password": password_checking
            })
    
    if result["okay"]:
        print("[s] : user created !")
        input("((press enter))")
        LOGO.effect_config.movement_speed = 10
        main()
    else:
        print(f"[s] : {result.data["error"]}")
        register()

def login():
    global is_logged_in
    global username_checking
    username_checking = input("username: ")

    if username_checking == "/exit":
        LOGO.effect_config.movement_speed = 500
        main()

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
        main()
    else:
        print("[s] : invalid username or password")
        login()

def main():
    clear_screen()
    if not client.connected:
        client.connect(s, transports=["polling"], wait_timeout=20)
    global is_logged_in

    if is_logged_in == False:

        with LOGO.terminal_output() as terminal:
            for frame in LOGO:
                terminal.print(frame)

        LRD = input("#: ")

        clear_screen()

        if LRD == "1":
            login()
        elif LRD == "2":
            register()
        else:
            print("[s] : invalid option")
            exit()

    clear_screen()
    with WELCOME.terminal_output() as terminal:
        for frame in WELCOME:
            terminal.print(frame)

    load_messages()

    while True:
        content = my_prompt()

        if content == "/exit":
            break

        if not content.strip():
            continue

        client.emit("msg", {
            "username" : username_checking,
            "content" : content
        })

if __name__ == "__main__":
    main()
