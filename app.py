# framework
from flask import Flask, request, render_template, redirect
import os
# game
from random import shuffle
from time import sleep
# client GET POST
import json
# server respond
from threading import Thread
# ui
from tkinter import *
from tkinter import messagebox, font

#    ██████╗  █████╗ ███╗   ███╗███████╗    ████████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ 
#   ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗
#   ██║  ███╗███████║██╔████╔██║█████╗         ██║   ███████║██████╔╝█████╗  ███████║██║  ██║
#   ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝         ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══██║██║  ██║
#   ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗       ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝
#    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
questions = []
with open("questions.json") as file:
    questions = json.load(file)

requests = []
declined = []
players = {}

answer_count = 0
current_question = 0
gamestart = False

## game var
question = "chim"
A = "yes"
B = "yes"
C = "yes"
D = "no"
layout = 4
ans_time = 30
answer = "D"

def check_answer_thread():
    global gamestart
    sleep(ans_time + 1)
    for name in list(players.keys()):
        if players[name]["current_ans"] == answer:
            players[name]["score"] += players[name]["ans_on"]
    gamestart = False
    nextbutton["state"] = "normal"
    current_work["text"] = "ended"

    if answer != "A":
        bA.pack_forget()
    if answer != "B":
        bB.pack_forget()
    if answer != "C":
        bC.pack_forget()
    if answer != "D":
        bD.pack_forget()

def delete_declined(name):
    sleep(1)
    declined.remove(name)

def player_count() -> int:
    return len(list(players.keys()))

#    ██████╗ ██╗   ██╗██╗
#   ██╔════╝ ██║   ██║██║
#   ██║  ███╗██║   ██║██║
#   ██║   ██║██║   ██║██║
#   ╚██████╔╝╚██████╔╝██║
#    ╚═════╝  ╚═════╝ ╚═╝

root_destroyed = False
root = Tk()
root.title("yes")
root.geometry("800x600")

tkfont = font.Font(family = "calibri", size = 25)
button_text_color = "#ffffff"

a_img = PhotoImage(file = "static/buttons/A.png")
b_img = PhotoImage(file = "static/buttons/B.png")
c_img = PhotoImage(file = "static/buttons/C.png")
d_img = PhotoImage(file = "static/buttons/D.png")

current_showing_image = PhotoImage(file = "static/image/blank.png")

question_label = Label(root, text = "cheap kahoot copy", font = tkfont, height = 3)
question_label.pack()

question_image = Label(root, image = current_showing_image)
question_image.image = current_showing_image
question_image.pack()

ans_frame = Frame(root)
ans_frame.pack(expand = True, fill = BOTH)

top_frame = Frame(ans_frame)
top_frame.pack(side = TOP, expand = True, fill = BOTH)

bottom_frame = Frame(ans_frame)
bottom_frame.pack(side = BOTTOM, expand = True, fill = BOTH)

bA = Label(top_frame, text = "A", font = tkfont, image = a_img, compound = CENTER, fg = button_text_color)
bA.pack(fill = BOTH, expand = True, side = LEFT)

bB = Label(top_frame, text = "B", font = tkfont, image = b_img, compound = CENTER, fg = button_text_color)
bB.pack(fill = BOTH, expand = True, side = RIGHT)

bC = Label(bottom_frame, text = "C", font = tkfont, image = c_img, compound = CENTER, fg = button_text_color)
bC.pack(fill = BOTH, expand = True, side = LEFT)

bD = Label(bottom_frame, text = "D", font = tkfont, image = d_img, compound = CENTER, fg = button_text_color)
bD.pack(fill = BOTH, expand = True, side = RIGHT)

##### control window #####
control_w = Toplevel(root)
control_w.title("control")
control_w.geometry("300x50")

current_work = Label(control_w, text = "no work")
current_work.pack()

def start_game():
    # reset
    bA.pack(fill = BOTH, expand = True, side = LEFT)
    bB.pack(fill = BOTH, expand = True, side = RIGHT)
    bC.pack(fill = BOTH, expand = True, side = LEFT)
    bD.pack(fill = BOTH, expand = True, side = RIGHT)
    bottom_frame.pack(side = TOP, expand = True, fill = BOTH)
    current_showing_image = PhotoImage(file = "static/image/blank.png")

    global gamestart, A, B, C, D, ans_time, current_ans, answer

    _question = questions[current_question]
    _answer = _question["answer"]
    _other_answer = _question["other_answer"]
    _image = _question["image"]
    choice_list = list(_other_answer) + [_answer]

    shuffle(choice_list)
    while len(choice_list) < 4:
        choice_list.append("NULL")
    A = choice_list[0]
    B = choice_list[1]
    C = choice_list[2]
    D = choice_list[3]

    if _image != "no":
        current_showing_image = PhotoImage(file = _image)

    question_label["text"] = _question["question"]
    question_image["image"] = current_showing_image
    question_image.image = current_showing_image
    bA["text"] = "A. " + A
    bB["text"] = "B. " + B
    bC["text"] = "C. " + C
    bD["text"] = "D. " + D

    if C == "NULL":
        bC.pack_forget()
    if D == "NULL":
        bD.pack_forget()
    if C == D and C == "NULL":
        bottom_frame.pack_forget()

    if   A == _answer: answer = 'A'
    elif B == _answer: answer = 'B'
    elif C == _answer: answer = 'C'
    elif D == _answer: answer = 'D'

    ans_time = int(questions[current_question]["time"])
    gamestart = True

    cat = Thread(target = check_answer_thread)
    cat.start()
    startbutton["state"] = "disabled"
    nextbutton["state"] = "disabled"
    current_work["text"] = "game started, waiting for " + str(ans_time) + 's'
def next_q():
    global current_question
    if len(questions) <= current_question + 1:
        reset = messagebox.askokcancel(title = "confirm", message = "out of question, restart?")
        if reset:
            current_question = 0
        else:
            return
    else:
        current_question += 1
    start_game()
startbutton = Button(control_w, text = "start", command = start_game)
startbutton.pack(side = "left")
nextbutton = Button(control_w, text = "next", command = next_q)
nextbutton.pack(side = "left")
    
####### request handling #####
def update_request():
    global root_destroyed
    while not root_destroyed:
        root.update()
        if len(requests) == 0: continue
        for name in requests:
            accept = messagebox.askyesno(title = "confirm", message = "accept " + name + "?")
            if accept:
                players[name] = {
                    "score": 0,
                    "current_ans": "N",
                    "ans_on": 30.0,
                }
            else:
                if name not in declined:
                    declined.append(name)
                    t = Thread(target = delete_declined, args = (name))
            requests.remove(name)
update_request_thread = Thread(target = update_request)
update_request_thread.start()
##########################

def on_quit():
    global root_destroyed
    root_destroyed = True
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_quit)

#   ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
#   ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
#   ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
#   ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
#   ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
#   ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═

app = Flask("cheap kahoot copy")

# "sign in" page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/game/<name>')
def add_player(name):
    return render_template("game.html", name = name)

@app.post("/player_request")
def make_request():
    name = request.json["name"]
    if name not in requests:
        requests.append(name)
    return ""

@app.post("/clear_player")
def clear_player():
    name = request.json["name"]
    players.pop(name)
    return ""

# get player and declined player list
@app.get("/players")
def get_players():
    return json.dumps(
        {
            "players": list(players.keys()),
            "declined": declined
        }
    )

# get players info
@app.get("/playersinfo")
def get_players_info():
    return json.dumps(players)

# get game state
@app.get("/gamestate")
def get_game_state():
    gamestate = {
        "start": gamestart,
        "question": questions[current_question]["question"],
        "a": A,
        "b": B,
        "c": C,
        "d": D,
        "layout": len(questions[current_question]["other_answer"]) + 1,
        "time": questions[current_question]["time"],
    }
    return json.dumps(gamestate)

@app.post("/post_answer")
def set_ans():
    name = request.json["name"]
    ans = request.json["ans"]
    ttt = request.json["time"]
    players[name]["current_ans"] = ans
    players[name]["ans_on"] = ttt
    return ""



def server():
    app.run(host = "0.0.0.0")
server_thread = Thread(target = server)
server_thread.start()
root.mainloop()
