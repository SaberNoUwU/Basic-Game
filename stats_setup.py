import pandas as pd 
from tkinter import * 

def STATS_SETUP(STATS_FRAME, a):
    HP_FRAME = Label(STATS_FRAME, bg="white", text=("HP: " + str(a[2])), font=("Arial", 8))
    HP_FRAME.pack(anchor="nw")
    ATK_FRAME = Label(STATS_FRAME, bg="white", text=("ATK: " + str(a[3])), font=("Arial", 8))
    ATK_FRAME.pack(anchor="nw")
    DEF_FRAME = Label(STATS_FRAME, bg="white", text=("DEF: " + str(a[4])), font=("Arial", 8))
    DEF_FRAME.pack(anchor="nw")
    CRT_FRAME = Label(STATS_FRAME, bg="white", text=("CRT: " + str(a[5])), font=("Arial", 8))
    CRT_FRAME.pack(anchor="nw")
    CDM_FRAME = Label(STATS_FRAME, bg="white", text=("CDM: " + str(a[6])), font=("Arial", 8))
    CDM_FRAME.pack(anchor="nw")
    INT_FRAME = Label(STATS_FRAME, bg="white", text=("INT: " + str(a[7])), font=("Arial", 8))
    INT_FRAME.pack(anchor="nw")
    MAG_FRAME = Label(STATS_FRAME, bg="white", text=("MAG: " + str(a[8])), font=("Arial", 8))
    MAG_FRAME.pack(anchor="nw")
    RES_FRAME = Label(STATS_FRAME, bg="white", text=("RES: " + str(a[9])), font=("Arial", 8))
    RES_FRAME.pack(anchor="nw")
    INS_FRAME = Label(STATS_FRAME, bg="white", text=("INS: " + str(a[10])), font=("Arial", 8))
    INS_FRAME.pack(anchor="nw")