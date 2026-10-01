from terminaltexteffects.effects.effect_binarypath import BinaryPath
from terminaltexteffects.effects.effect_expand import Expand
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

┌── THE RULES ──────────────────────────────────────────────────────────────────────┐
│                                                                                   │
│ * this chat was created with the intention of give you the oportunity to share    │
│   your ideas and talk about random stuff.                                         │
│ * does not mean that you will not be punished if you disrespect the order of our  │ 
│   members.                                                                        │
│ * the creator of the chat liked the project so much that he decided to choose two │
│   awesome administrators to rule the chat                                         │
│                                                                                   │
│       ┌───────────────────────────────────────────────────────────────────┐       │
│       │                              ADMINS:                              │       │
│       │ 1. Matheus Henrique [br] @troy                                    │       │
│       │ 2. João Nunes [pt] @cogito                                        │       │
│       │ 3. Martim Gabriel [pt] @mafanhoto                                 │       │
│       └───────────────────────────────────────────────────────────────────┘       │
│                                                                                   │
│ 1 -- | DO NOT FLOOD                                                               │
│ 2 -- | DO NOT BULLY                                                               │
│ 3 -- | DO NOT SPAM                                                                │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
"""

WELCOME = Expand(WELCOME_TEXT)

LOGO = BinaryPath(LOGO_TEXT)
LOGO.terminal_config.canvas_width = -1
LOGO.terminal_config.canvas_height = -1
LOGO.effect_config.movement_speed = 2

import os

@staticmethod
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

import sys
import socketio
import server

client = socketio.Client()
s = "http://127.0.0.1:5555"

is_logged_in = False
sc_username = ""

@client.event
def connect():
    print("[s] : connected to the server")

@client.event
def disconnect():
    print("[s] : disconnected from the server")

@staticmethod
def register():
    username = input("username: ")

    if username == "/exit":
        LOGO.effect_config.movement_speed = 10
        main()

    if username == None:
        print("[s] : please enter your username")
        register()
    elif len(username)<3:
        print("[s] : your username must be at least 3 characters")
        register()
    elif server.if_user_exists(username):
        print("[s] : user already exists")
        register()
    else:
        password = input("password: ")
        if password == None:
            print("[s] : please enter your password")
            register()
        elif len(password)<3:
            print("[s] : your password must be at least 3 characters")
            register()
        else:
            server.create_user(username, password)
            print("[s] : user created successfully")
            LOGO.effect_config.movement_speed = 10
            main()

def login():
    global is_logged_in
    global sc_username
    username = input("username: ")

    if username == "/exit":
        LOGO.effect_config.movement_speed = 500
        main()

    if not server.if_user_exists(username):
        print("[s] : user does not exist")
        login()
    else:
        password = input("password: ")
        if server.if_password_match(username, password):
            is_logged_in = True
            print("[s] : welcome!")
            sc_username = username
            LOGO.effect_config.movement_speed = 10
            main()
        else:
            print("[s] : invalid username or password")
            login()


def main():
    clear_screen()

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

    client.connect(s)

    while True:
        content = input("@: ")

        sys.stdout.write("\033[1A\033[2K\r")
        sys.stdout.flush()

        if content == "/exit":
            break

        server.msg(sc_username, content)

if __name__ == "__main__":
    main()