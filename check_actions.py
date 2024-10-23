from tkinter import *

def CHECK_ACTIONS(ENERGY, IS_CLICK): 
    if (ENERGY == 0): 
        return "disabled"
    return "active"