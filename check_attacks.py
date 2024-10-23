from tkinter import *

def CHECK_ATTACKS(ENERGY, IS_CLICK): 
    if (ENERGY <= 1) or (IS_CLICK == 1): 
        return "disabled"
    return "active"