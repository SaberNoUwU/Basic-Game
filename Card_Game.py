import pandas as pd
import random
from tkinter import *
import time
from check_attacks import CHECK_ATTACKS
from check_actions import CHECK_ACTIONS
from stats_setup import STATS_SETUP

# NOTE: SINGLE PLAYER OFFLINE ONLY FOR NOW (MAX_PLAYER = 1)
#       DO MULTIPLAYER OFFLINE ON LATER TIME (MAX_PLAYER > 1)

# SETTING UP SCREEN
window = Tk()
Width = 1600  # WIDTH OF YOUR SCREEN
Height = 900  # HEIGHT OF YOUR SCREEN
window.geometry("1600x900")
my_canvas = Canvas(window, width=Width, height=Height, bg="black")
my_canvas.pack()

# PANDAS SETTING
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 0)

# STATS + TITLE
NAME, TITLE = "", ""
HP, ATK, DEF, CRT, CDM, INT, MAG, RES, INS = 0, 0, 0, 0, 0, 0, 0, 0, 0

CHARS_LIST = []  # LIST OF CHARACTERS NAME, TITLE AND STATS
FRAME_LIST = []  # LIST OF FRAMES USING
ENERGY_BTN_LIST = []  # LIST OF ENERGY FRAMES USING
BTN_LIST = []  # LIST OF BUTTONS USING
TEAM = []  # IDs OF CHARACTERS IN A TEAM
ACTIVE_ID = []  # IDs OF ACTIVE CHARACTERS ON THE FIELD
MAX_PLAYER = 0  # NUMBER OF PLAYERS WE TAKE
CURRENT_CLICK, TEAM_COUNT = -1, 0  # CHECK WHAT WIDGET WE CLICKED ON, NUMBER OF TEAMMATES ON A TEAM
CLICK_AMOUNT = 0  # HOW MANY MOUSE BUTTONS HAS BEEN CLICKED
NUM_CHAR_FRAMES = 0  # NUMBER OF CHARACTERS FRAMES
DAMAGE = 0  # DAMAGE VALUE
CURRENT_ENERGY = 3  # HOW MANY ENERGY ARE LEFT

# VARIABLES TO CHECK IF A BUTTON IS PRESSED OR NOT
IS_CLICK_NORM_ATTACK, IS_CLICK_MAG_ATTACK, IS_CLICK_SPE_ATTACK, IS_CLICK_INS_ATTACK = 0, 0, 0, 0
IS_CLICK_SAVE, IS_CLICK_ENDTURN, IS_CLICK_ENDPHASE, IS_CLICK_CHANGE = 0, 0, 0, 0

# PSEUDO DICE100
DICE_100 = []
for i in range(100):
    DICE_100.append(i + 1)

# READ DATA FROM XLSX
dataframe = pd.read_excel('~/Character.xlsx', sheet_name="Character")  # Character infos
dataframe2 = pd.read_excel('~/Character.xlsx', sheet_name="Item")  # Item infos

# print(dataframe2)

# SETTING UP DATAS
for i in range(1, len(dataframe.columns) - 1):
    if dataframe.columns[i] != 'Unnamed: 8':
        CHARS_LIST.append([NAME, TITLE, HP, ATK, DEF, CRT, CDM, INT, MAG, RES, INS])
        CHARS_LIST[len(CHARS_LIST) - 1][0] = dataframe.columns[i]

# ADD STATS FOR CHARACTERS
for i in range(0, len(CHARS_LIST)):
    for j in range(0, 10):
        if j == 0:
            CHARS_LIST[i][j + 1] = dataframe.loc[j, CHARS_LIST[i][0]].replace("\n", "")
        else:
            CHARS_LIST[i][j + 1] = dataframe.loc[j, CHARS_LIST[i][0]]
    CHARS_LIST[i][0] = CHARS_LIST[i][0].replace("\n", "")

# GET DATA OF WIDGET WE CLICKED
def mouse_click(event=None):
    # SEND IN SOME VARIABLES
    global TEAM
    global CLICK_AMOUNT
    global NUM_CHAR_FRAMES
    global DAMAGE
    global IS_CLICK_NORM_ATTACK, IS_CLICK_MAG_ATTACK, IS_CLICK_SPE_ATTACK, IS_CLICK_INS_ATTACK
    global BTN_LIST
    global ACTIVE_ID
    global IS_CLICK_CHANGE

    # EXTRACT THE FRAME NUMBER
    temp = str(event.widget)
    temp += ".!"
    CURRENT_CLICK = -1
    if temp.find(".!frame") != -1:
        temp = temp.replace(".!frame", "", 1)
        temp2 = ""
        for i in range(0, temp.find(".!")):
            temp2 += temp[i]
        if temp2 == "":
            CURRENT_CLICK = 1
        else:
            CURRENT_CLICK = int(temp2)

    if CURRENT_CLICK != -1:
        # CHOOSING TEAM MEMBERS
        if (not (CURRENT_CLICK in TEAM)) and (CLICK_AMOUNT < 3):
            FRAME_LIST[CURRENT_CLICK - 1].destroy()
            TEAM.append(CURRENT_CLICK)
            CLICK_AMOUNT += 1
        # ATTACK USING NORMAL ATTACKS
        if len(ACTIVE_ID) > 0:
            if CURRENT_CLICK != ACTIVE_ID[0] and (CURRENT_CLICK in ACTIVE_ID) and IS_CLICK_NORM_ATTACK == 1:

                currhp_str = FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[0][
                    'text']
                # DAMAGE CALCULATION
                currhp_str = currhp_str.replace("HP: ", "")
                currhp_int = int(currhp_str)
                currdef_str = FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[2][
                    'text']
                currdef_str = currdef_str.replace("DEF: ", "")
                currdef_int = int(currdef_str)
                currhp_int = min(currhp_int - (DAMAGE - currdef_int), currhp_int)
                if currhp_int <= 0:
                    currhp_int = 0
                FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[0][
                    'text'] = "HP: " + str(currhp_int)
                # IS_CLICK_NORM_ATTACK = 0
                window.winfo_children()[len(window.winfo_children()) - 1].destroy()
                # ADD TO THE LOG
                if DAMAGE - currdef_int < 0:
                    DAMAGE = currdef_int
                LOG.config(state="normal")
                LOG.insert(END, (
                            FRAME_LIST[ACTIVE_ID[0] - MAX_PLAYER * 5 - 1].winfo_children()[0]['text'] + " deal " + str(DAMAGE - currdef_int) + " damage to " +
                            FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].winfo_children()[0]['text'] + "\n"))
                LOG.yview(END)
                LOG.config(state="disabled")
                # ACTIVATE REMAINING OPTIONS
                for btn in BTN_LIST:
                    if btn['text'] == "Normal Attack":
                        continue
                    else:
                        btn.config(state="active")
            if CURRENT_CLICK != ACTIVE_ID[0] and (1 + MAX_PLAYER * 5 <= CURRENT_CLICK <= 3 + MAX_PLAYER * 5) and IS_CLICK_CHANGE == 1:
                IS_CLICK_CHANGE = 0
                LEFT_X = FRAME_LIST[ACTIVE_ID[0] - MAX_PLAYER * 5 - 1].winfo_rootx()
                RIGHT_X = FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].winfo_rootx()
                FRAME_LIST[ACTIVE_ID[0] - MAX_PLAYER * 5 - 1].place(x=RIGHT_X, y=435)
                FRAME_LIST[CURRENT_CLICK - MAX_PLAYER * 5 - 1].place(x=LEFT_X, y=435)
                ACTIVE_ID[0] = CURRENT_CLICK
                for btn in BTN_LIST:
                    btn.config(state="active")

    # CHECK IF SAVE IS AVAILABLE OR NOT
    # NOTE: SAVE IS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_SAVE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); 

    # CHECK IF ATTACK OPTIONS ARE AVAILABLE OR NOT
    # NOTE: ATTACKS ONLY AVAILABLE IF CURRENT ENERGY > 1 AND HASN'T BEEN CLICKED IN TURN
    BTN_NORMAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_NORM_ATTACK))
    BTN_MAGIC_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_MAG_ATTACK))
    BTN_SPECIAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_SPE_ATTACK))
    BTN_INSANITY_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_INS_ATTACK))


    # CHECK IF MISCELLANEOUS OPTIONS ARE AVAILABLE OR NOT
    # NOTE: MISCELLANEOUS OPTIONS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_CHANGE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); ()
    BTN_EQUIP_ITEM.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); ()
    # print(CLICK_AMOUNT)
    # print(NUM_CHAR_FRAMES)


# PUTTING STATS ON FRAME
def CREATE_FRAME():
    global CLICK_AMOUNT
    global FRAME_LIST
    global NUM_CHAR_FRAMES
    i = 0
    NUM_CHAR_FRAMES = 0
    while i < MAX_PLAYER:
        if not FRAME_LIST:
            CURRENT_WIDTH = 0
            for j in range(i * 5, (i + 1) * 5):
                FRAME_LIST.append(Frame(window, bg="lightgray", width=100, height=100, bd=5))
                FRAME_LIST[len(FRAME_LIST) - 1].place(x=175 + CURRENT_WIDTH, y=200)
                NAME_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[j][0],
                                   font=("Arial", 9))
                NAME_FRAME.pack()
                TITLE_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[j][1],
                                    font=("Arial", 9))
                TITLE_FRAME.pack()
                AVATAR_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="gray", width=163, height=100)
                AVATAR_FRAME.pack()
                STATS_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="white", width=163, height=155)
                STATS_FRAME.pack()
                STATS_FRAME.pack_propagate(False)
                STATS_SETUP(STATS_FRAME, CHARS_LIST[j])
                Tk.update(window)
                CURRENT_WIDTH += FRAME_LIST[i].winfo_width() + 50
                NUM_CHAR_FRAMES += 1
        if CLICK_AMOUNT == 3:
            i += 1
            CLICK_AMOUNT = 0
            for j in range(len(FRAME_LIST)):
                FRAME_LIST[j].destroy()
            FRAME_LIST = []
            # print(MAX_PLAYER)
            print()
        Tk.update(window)


# RANDOMIZE CHARACTERS
random.shuffle(CHARS_LIST)
# print(CHARS_LIST)
MAX_PLAYER = input("Enter amount of players: ")
MAX_PLAYER = int(MAX_PLAYER)
window.bind("<Button-1>", mouse_click)
CREATE_FRAME()
CLICK_AMOUNT = 3
CURRENT_WIDTH = 0
# print(TEAM)
# PLAYER 1 CHARACTERS LIST
for i in range(len(TEAM)):
    FRAME_LIST.append(Frame(window, bg="lightgray", width=100, height=100, bd=5))
    FRAME_LIST[len(FRAME_LIST) - 1].place(x=450 + CURRENT_WIDTH, y=435)
    NAME_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[TEAM[i] - 1][0],
                       font=("Arial", 9))
    NAME_FRAME.pack()
    TITLE_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[TEAM[i] - 1][1],
                        font=("Arial", 9))
    TITLE_FRAME.pack()
    AVATAR_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="gray", width=163, height=100)
    AVATAR_FRAME.pack()
    STATS_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="white", width=163, height=155)
    STATS_FRAME.pack()
    STATS_FRAME.pack_propagate(False)
    STATS_SETUP(STATS_FRAME, CHARS_LIST[TEAM[i] - 1])
    CURRENT_WIDTH += 173
    NUM_CHAR_FRAMES += 1

# OPPONENT 1 CHARACTERS LIST
CURRENT_WIDTH = 0
for i in range(5, 8):
    FRAME_LIST.append(Frame(window, bg="lightgray", width=100, height=100, bd=5))
    FRAME_LIST[len(FRAME_LIST) - 1].place(x=0 + CURRENT_WIDTH, y=0)
    NAME_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[i][0],
                       font=("Arial", 9))
    NAME_FRAME.pack()
    TITLE_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[i][1],
                        font=("Arial", 9))
    TITLE_FRAME.pack()
    AVATAR_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="gray", width=163, height=100)
    AVATAR_FRAME.pack()
    STATS_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="white", width=163, height=155)
    STATS_FRAME.pack()
    STATS_FRAME.pack_propagate(False)
    STATS_SETUP(STATS_FRAME, CHARS_LIST[i])
    CURRENT_WIDTH += 173
    NUM_CHAR_FRAMES += 1

# OPPONENT 2 CHARACTERS LIST
CURRENT_WIDTH = 0
for i in range(10, 13):
    FRAME_LIST.append(Frame(window, bg="lightgray", width=100, height=100, bd=5))
    FRAME_LIST[len(FRAME_LIST) - 1].place(x=846 + CURRENT_WIDTH, y=0)
    NAME_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[i][0],
                       font=("Arial", 9))
    NAME_FRAME.pack()
    TITLE_FRAME = Label(FRAME_LIST[len(FRAME_LIST) - 1], bg="lightgray", text=CHARS_LIST[i][1],
                        font=("Arial", 9))
    TITLE_FRAME.pack()
    AVATAR_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="gray", width=163, height=100)
    AVATAR_FRAME.pack()
    STATS_FRAME = Frame(FRAME_LIST[len(FRAME_LIST) - 1], bg="white", width=163, height=155)
    STATS_FRAME.pack()
    STATS_FRAME.pack_propagate(False)
    STATS_SETUP(STATS_FRAME, CHARS_LIST[i])
    CURRENT_WIDTH += 173
    NUM_CHAR_FRAMES += 1

Tk.update(window)

# ACTIVE CHARACTER LIST
ACTIVE_ID = [6, 9, 12]

# CREATE ENERGY BAR (MAX 4E, 1ST TURN = 3E => 1st 3 bar = Yellow, last one = Gray
#                    NOTE: Yellow = Can use, Gray = Already used/Cannot use)
ENERGY_BAR = Frame(window, bg="lightgray", width=100, height=100, bd=5)
ENERGY_BAR.place(x=0, y=457)
ENERGY_LABEL = Label(ENERGY_BAR, text="Energy  ", font=("Arial", 9))
ENERGY_LABEL.pack(side=LEFT)
for i in range(4):
    ENERGY_BTN_LIST.append(Button(ENERGY_BAR, bg="yellow", width=7, height=1, bd=1, state="disabled"))
    ENERGY_BTN_LIST[len(ENERGY_BTN_LIST) - 1].pack(side=LEFT)

for i in range(CURRENT_ENERGY, 4):
    ENERGY_BTN_LIST[i].config(bg="gray")


def NORMAL_ATTACK_FRAME():
    # SEND IN SOME VARIABLES
    global DAMAGE
    global IS_CLICK_NORM_ATTACK
    global BTN_LIST
    global CURRENT_ENERGY

    # NORMAL ATTACK = 2E
    CURRENT_ENERGY -= 2
    for i in range(CURRENT_ENERGY, 4):
        ENERGY_BTN_LIST[i].config(bg="gray")

    # DISABLE BUTTON OPTIONS
    for btn in BTN_LIST:
        btn.config(state="disabled")

    IS_CLICK_NORM_ATTACK = 1
    NORM_ATK_FRAME = Frame(window, bg="lightgray", width=100, height=100, bd=5)
    NORM_ATK_FRAME.place(x=620, y=50)
    NAME_NORM_ATK_FRAME = Label(NORM_ATK_FRAME, text="Normal Attack", font=("Arial", 9))
    NAME_NORM_ATK_FRAME.pack()
    AVATAR_NORM_ATK_FRAME = Frame(NORM_ATK_FRAME, bg="gray", width=130, height=100)
    AVATAR_NORM_ATK_FRAME.pack()
    DESC_NORM_ATK_FRAME = Frame(NORM_ATK_FRAME, bg="white", width=130, height=100)
    DESC_NORM_ATK_FRAME.pack()
    DAMAGE = CHARS_LIST[TEAM[0] - 1][3]
    random.shuffle(DICE_100)
    if DICE_100[0] <= CHARS_LIST[TEAM[0] - 1][5]:  # CHECK IF CRIT OR NOT
        DAMAGE = DAMAGE * CHARS_LIST[TEAM[0] - 1][6] / 100
        DAMAGE += 0.5
        DAMAGE = int(DAMAGE)
    DESC = Label(DESC_NORM_ATK_FRAME, text=("Deal " + str(DAMAGE) + " damage"))  # VISUALIZE THE DAMAGE POTENTIAL
    DESC.pack()
    # ADD TO THE LOG
    LOG.config(state="normal")
    LOG.insert(END,
               (FRAME_LIST[ACTIVE_ID[0] - MAX_PLAYER * 5 - 1].winfo_children()[0]['text'] + " use Normal Attack \n"))
    LOG.yview(END)
    LOG.config(state="disabled")


def SAVE():
    global CURRENT_ENERGY
    if CURRENT_ENERGY > 0:
        CURRENT_ENERGY = 4
    else:
        CURRENT_ENERGY = 3
    for i in range(4):
        ENERGY_BTN_LIST[i].config(bg="gray")
    for btn in BTN_LIST:
        btn.config(state="disabled")
    Tk.update(window)
    ENEMY_TURN()
    time.sleep(1)
    for i in range(CURRENT_ENERGY):
        ENERGY_BTN_LIST[i].config(bg="yellow")
    for btn in BTN_LIST:
        btn.config(state="active")

    # CHECK IF SAVE IS AVAILABLE OR NOT
    # NOTE: SAVE IS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_SAVE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); 

    # CHECK IF ATTACK OPTIONS ARE AVAILABLE OR NOT
    # NOTE: ATTACKS ONLY AVAILABLE IF CURRENT ENERGY > 1
    BTN_NORMAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_NORM_ATTACK))
    BTN_MAGIC_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_MAG_ATTACK))
    BTN_SPECIAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_SPE_ATTACK))
    BTN_INSANITY_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_INS_ATTACK))

    # CHECK IF MISCELLANEOUS OPTIONS ARE AVAILABLE OR NOT
    # NOTE: MISCELLANEOUS OPTIONS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_CHANGE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); ()
    BTN_EQUIP_ITEM.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); ()


# ONLY DOING NORMAL ATTACKS FOR NOW
# FUTURE UPDATE v1: COULD DO SPECIAL, MAGIC, INSANITY ATTACK
# FUTURE UPDATE v2: DO TURNS OPTIMALLY
def ENEMY_TURN():
    global DAMAGE
    global IS_CLICK_NORM_ATTACK
    global BTN_LIST
    global CURRENT_ENERGY
    global ACTIVE_ID

    for i in range(2):
        NORM_ATK_FRAME = Frame(window, bg="lightgray", width=100, height=100, bd=5)
        NORM_ATK_FRAME.place(x=620, y=50)
        NAME_NORM_ATK_FRAME = Label(NORM_ATK_FRAME, text="Normal Attack", font=("Arial", 9))
        NAME_NORM_ATK_FRAME.pack()
        AVATAR_NORM_ATK_FRAME = Frame(NORM_ATK_FRAME, bg="gray", width=130, height=100)
        AVATAR_NORM_ATK_FRAME.pack()
        DESC_NORM_ATK_FRAME = Frame(NORM_ATK_FRAME, bg="white", width=130, height=100)
        DESC_NORM_ATK_FRAME.pack()
        if i == 0:
            CURRENT_CHARACTER = 5
        else:
            CURRENT_CHARACTER = 10
        DAMAGE = CHARS_LIST[CURRENT_CHARACTER][3]
        random.shuffle(DICE_100)
        if DICE_100[0] <= CHARS_LIST[CURRENT_CHARACTER][5]:  # CHECK IF CRIT OR NOT
            DAMAGE = DAMAGE * CHARS_LIST[CURRENT_CHARACTER][6] / 100
            DAMAGE += 0.5
            DAMAGE = int(DAMAGE)
        DESC = Label(DESC_NORM_ATK_FRAME, text=("Deal " + str(DAMAGE) + " damage"))  # VISUALIZE THE DAMAGE POTENTIAL
        DESC.pack()
        # ADD TO THE LOG
        LOG.config(state="normal")
        LOG.insert(END, (CHARS_LIST[CURRENT_CHARACTER][0] + " use Normal Attack \n"))
        LOG.config(state="disabled")
        Tk.update(window)
        random.shuffle(DICE_100)
        CHAR_GET_HIT = 0
        if i == 0:
            if DICE_100[0] % 2 == 0:
                CHAR_GET_HIT = ACTIVE_ID[0]
            else:
                CHAR_GET_HIT = ACTIVE_ID[2]
        else:
            if DICE_100[0] % 2 == 0:
                CHAR_GET_HIT = ACTIVE_ID[0]
            else:
                CHAR_GET_HIT = ACTIVE_ID[1]
        currhp_str = FRAME_LIST[CHAR_GET_HIT - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[0]['text']
        # DAMAGE CALCULATION
        currhp_str = currhp_str.replace("HP: ", "")
        currhp_int = int(currhp_str)
        currdef_str = FRAME_LIST[CHAR_GET_HIT - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[2]['text']
        currdef_str = currdef_str.replace("DEF: ", "")
        currdef_int = int(currdef_str)
        currhp_int = min(currhp_int - (DAMAGE - currdef_int), currhp_int)
        if currhp_int <= 0:
            currhp_int = 0
        FRAME_LIST[CHAR_GET_HIT - MAX_PLAYER * 5 - 1].winfo_children()[3].winfo_children()[0]['text'] = "HP: " + str(
            currhp_int)
        # ADD TO THE LOG
        if DAMAGE - currdef_int < 0:
            DAMAGE = currdef_int
        LOG.config(state="normal")
        LOG.insert(END, (FRAME_LIST[ACTIVE_ID[i + 1] - MAX_PLAYER * 5 - 1].winfo_children()[0]['text'] + " deal " + str(
            DAMAGE - currdef_int) + " damage to " +
                         FRAME_LIST[CHAR_GET_HIT - MAX_PLAYER * 5 - 1].winfo_children()[0]['text'] + "\n"))
        LOG.yview(END)
        LOG.config(state="disabled")
        window.winfo_children()[len(window.winfo_children()) - 1].destroy()
        time.sleep(5)


def END_TURN():
    global CURRENT_ENERGY
    CURRENT_ENERGY = 3
    for i in range(4):
        ENERGY_BTN_LIST[i].config(bg="gray")
    for btn in BTN_LIST:
        btn.config(state="disabled")
    Tk.update(window)
    time.sleep(1)
    ENEMY_TURN()
    for i in range(3):
        ENERGY_BTN_LIST[i].config(bg="yellow")
    for btn in BTN_LIST:
        btn.config(state="active")

    # CHECK IF SAVE IS AVAILABLE OR NOT
    # NOTE: SAVE IS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_SAVE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); 

    # CHECK IF ATTACK OPTIONS ARE AVAILABLE OR NOT
    # NOTE: ATTACKS ONLY AVAILABLE IF CURRENT ENERGY > 1
    BTN_NORMAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_NORM_ATTACK))
    BTN_MAGIC_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_MAG_ATTACK))
    BTN_SPECIAL_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_SPE_ATTACK))
    BTN_INSANITY_ATTACK.config(state=CHECK_ATTACKS(CURRENT_ENERGY, IS_CLICK_INS_ATTACK))

    # CHECK IF MISCELLANEOUS OPTIONS ARE AVAILABLE OR NOT
    # NOTE: MISCELLANEOUS OPTIONS ONLY AVAILABLE IF CURRENT ENERGY > 0
    BTN_CHANGE.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); 
    BTN_EQUIP_ITEM.config(state=CHECK_ACTIONS(CURRENT_ENERGY)); 


def END_PHASE():
    global CURRENT_ENERGY
    global IS_CLICK_NORM_ATTACK, IS_CLICK_MAG_ATTACK, IS_CLICK_SPE_ATTACK, IS_CLICK_INS_ATTACK
    CURRENT_ENERGY = 3
    for i in range(4):
        ENERGY_BTN_LIST[i].config(bg="gray")
    for btn in BTN_LIST:
        btn.config(state="disabled")
    Tk.update(window)
    time.sleep(1)
    for i in range(3):
        ENERGY_BTN_LIST[i].config(bg="yellow")
    for btn in BTN_LIST:
        btn.config(state="active")
    IS_CLICK_NORM_ATTACK = 0
    IS_CLICK_MAG_ATTACK = 0
    IS_CLICK_SPE_ATTACK = 0
    IS_CLICK_INS_ATTACK = 0


def CHANGE():
    global IS_CLICK_CHANGE
    global CURRENT_ENERGY

    # CHANGE = 1E
    CURRENT_ENERGY -= 1
    for i in range(CURRENT_ENERGY, 4):
        ENERGY_BTN_LIST[i].config(bg="gray")

    # DISABLE BUTTON OPTIONS
    for btn in BTN_LIST:
        btn.config(state="disabled")

    IS_CLICK_CHANGE = 1


# BATTLE LOG
BATTLE_LOG_FRAME = Frame(window, height=5, width=40)
BATTLE_LOG_FRAME.place(x=1000, y=315)
SCROLL_BAR = Scrollbar(BATTLE_LOG_FRAME)
LOG = Text(BATTLE_LOG_FRAME, height=5, width=40, yscrollcommand=SCROLL_BAR.set)
SCROLL_BAR.config(command=LOG.yview)
SCROLL_BAR.pack(side=RIGHT, fill=Y)
LOG.pack(side=LEFT)
LOG.insert(END, "Log: \n")

# MAKE TEXt BOX READ-ONLY
# NOTE: PUT THIS BEHIND THE CODE THAT INSERTS TEXT TO THE TEXT BOX
# LOG.config(state="disabled")

# ATTACKS OPTIONS
BTN_NORMAL_ATTACK = Button(window, text="Normal Attack", font=("Arial", 9), command=NORMAL_ATTACK_FRAME)
BTN_NORMAL_ATTACK.place(x=0,
                        y=500)
Tk.update(window)
BTN_MAGIC_ATTACK = Button(window, text="Magic Attack", font=("Arial", 9))
BTN_MAGIC_ATTACK.place(x=BTN_NORMAL_ATTACK.winfo_width(),
                       y=500)
Tk.update(window)
BTN_SPECIAL_ATTACK = Button(window, text="Special Attack", font=("Arial", 9))
BTN_SPECIAL_ATTACK.place(x=BTN_NORMAL_ATTACK.winfo_width() + BTN_MAGIC_ATTACK.winfo_width(),
                         y=500)
Tk.update(window)
BTN_INSANITY_ATTACK = Button(window, text="Insanity Attack", font=("Arial", 9))
BTN_INSANITY_ATTACK.place(
    x=BTN_NORMAL_ATTACK.winfo_width() + BTN_MAGIC_ATTACK.winfo_width() + BTN_SPECIAL_ATTACK.winfo_width(),
    y=500)
Tk.update(window)

# TURNS/PHASES OPTIONS
BTN_SAVE = Button(window, text="Save", font=("Arial", 9), command=SAVE)
BTN_SAVE.place(x=0, y=500 + BTN_NORMAL_ATTACK.winfo_height())
Tk.update(window)
BTN_END_TURN = Button(window, text="End Turn", font=("Arial", 9), command=END_TURN)
BTN_END_TURN.place(x=BTN_SAVE.winfo_width(), y=500 + BTN_NORMAL_ATTACK.winfo_height())
Tk.update(window)
BTN_END_PHASE = Button(window, text="End Phase", font=("Arial", 9), command=END_PHASE)
BTN_END_PHASE.place(x=BTN_SAVE.winfo_width() + BTN_END_TURN.winfo_width(), y=500 + BTN_NORMAL_ATTACK.winfo_height())
Tk.update(window)

# MISCELLANEOUS OPTIONS
BTN_CHANGE = Button(window, text="Change", font=("Arial", 9), command=CHANGE)
BTN_CHANGE.place(x=0, y=500 + 2*BTN_NORMAL_ATTACK.winfo_height())
Tk.update(window)
BTN_EQUIP_ITEM = Button(window, text="Equip", font=("Arial", 9))
BTN_EQUIP_ITEM.place(x=BTN_CHANGE.winfo_width(), y=500 + 2*BTN_NORMAL_ATTACK.winfo_height())
Tk.update(window)

# PUT ALL BUTTONS INTO A LIST
BTN_LIST.append(BTN_NORMAL_ATTACK)
BTN_LIST.append(BTN_MAGIC_ATTACK)
BTN_LIST.append(BTN_SPECIAL_ATTACK)
BTN_LIST.append(BTN_INSANITY_ATTACK)
BTN_LIST.append(BTN_SAVE)
BTN_LIST.append(BTN_END_TURN)
BTN_LIST.append(BTN_END_PHASE)
BTN_LIST.append(BTN_CHANGE)
BTN_LIST.append(BTN_EQUIP_ITEM)

# CHECK IF SAVE IS AVAILABLE OR NOT
# NOTE: SAVE IS ONLY AVAILABLE IF CURRENT ENERGY > 0
# CHECK_SAVE_AVAILABLE()

window.mainloop()
