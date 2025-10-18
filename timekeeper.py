# Author Justin Holley
# CS361 - Fall 2025

# UI currently works exclusively for windows based systems. 

# IMPORTED LIBRARIES
import os
import msvcrt
from datetime import datetime

# GLOBALS
EMP_FILE = "employees.json"


KEYMAP = {
    '3b': 'F1',
    '48': 'UP',
    '50': 'DOWN',
    '4b': 'LEFT',
    '4d': 'RIGHT'
}

KEYS = ['F1',
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT']

# VARIABLE GLOBALS
Cur_Entry = ''       # Used to track the users current entry
Employees = {}          # Dictionary to create employees
Screen = "main_menu"    # Used to specify what screen to go to

# Temporary Globals DELETE WHEN DONE
    # Temporary Employees Dictionary until one exists
Employees['1234'] = {   
    "first": "Elmer",
    "last": "Fudd",
    "wage":  "20.00",
    "clocked_in": False,
    "last_clock_in": None,
    "time_cards": []
}





"""Function that gets keys pressed on keyboard by the user"""
def getchar():
    ch = msvcrt.getch()
    
    # handle if a special key was pressed that has a prefix byte (i.e. arrows,
    # F1, F2, etc. - these keys will all have two byes that are read and the 
    # first byte will be the hex value x00 or xe0)
    if ch in (b'\x00', b'\xe0'):
        # get the second character to determine if it's a special key 
        # that I want to deal with. 
        ch2 = msvcrt.getch()
        code = ch2.hex()
        return KEYMAP.get(code, 'IGNORE')
    return ch.decode('utf', errors='ignore') 


"""
Function that gets a users input and returns it when they press enter. 
If the user presses Escape, program returns without returning an entry
"""
def getentry():
    entry = ''
    while True:
        ch = getchar()
        
        # If the entry is a keyboard button to ignore:
        if ch == 'IGNORE':
            continue
        
        if ch in KEYS:
            continue

        # If Entry is Escape Key
        if ch == '\x1b':
            return          
        
        # If Entry is Backspace
        if ch == '\x08':
            if len(entry) > 0:
                entry = entry[:-1] # remove last character
                # move cursor back, print space over it, move cursor back again
                print("\b \b", end="", flush=True) 

        # if the character is printable, add it to the Cur_Entry
        if ch.isprintable():
            entry += ch
            print(f'{ch}', end="", flush=True)

        # if Entry is Enter
        if ch == '\r':
            print("", end="\n", flush=False)
            return entry           

def _new_clock_in(entry):
        f_name = Employees[entry]['first']
        l_name = Employees[entry]['last']
        time = datetime.now()
        card = {
                'cit': datetime.now(), 
                'cot': "",
                'hrs': ""
                }
        Employees[entry]['time_cards'].append(card)
        Employees[entry]['clocked_in'] = True
        Employees[entry]['last_clock_in'] = time
        # time = Employees[Cur_Entry]['time_cards'][-1]['cit']
        print(f'\n{f_name} {l_name} HAS CLOCKED IN AT {time}')

"""Main Menu Screen"""
def main_menu():
    os.system('cls') # Clear Screen
    print("\t\t\t\tWELCOME TO TIMEKEEPER!")
    print("\t\tThe Program that tracks your work hours so you can get paid!\n")
    print("MAIN MENU\n")
    print("Select a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard:")
    print("(1)\tCLOCK IN")
    print("(2)\tCLOCK OUT")
    print("(3)\tSUPERVISOR MENU")
    print("(4)\tQUIT")
    print("\n\"Clock In\" tracks when you start work, \"Clock out\" tracks "
          "when you stop work. Each takes less than a minute to help ensure "
          "you are paid for your hard work!")
    print("\nNot sure if you're clocked in or out? Don't worry! You can try "
          "clocking in or clocking out again and the program will tell you if "
          "you are already clocked in or out!")
    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == "1":
            return "clock_in"       
        if Cur_Entry == "4":
            return "_quit_"
    


""" Clock In Screen """
def clock_in():
    os.system('cls')    # Clear Screen
    Cur_Entry = ''   # Clear Cur_Entry for use in this screen.  
    
    print("CLOCK IN\n")
    print("Clocking in tracks when you start work.\n")
    print("INSTRUCTIONS:")
    print("To Clock in for work, please enter your Employee ID and Press "
          "Enter.")
    print("To return to the Main Menu, press the Escape key (Esc).")
    print("\nNot sure if you're clocked in or out? Don't worry! You can try "
        "clocking in or clocking out again and the program will tell you if "
        "you are already clocked in or out!")
    
    print("\nPlease enter your Employee ID: ", end="", flush=True)
    
    Cur_Entry = getentry()

    if Cur_Entry in Employees and Employees[Cur_Entry]["clocked_in"]:
        f_name = Employees[Cur_Entry]['first']
        l_name = Employees[Cur_Entry]['last']
        print(f'{f_name} {l_name} is already clocked in!')
        print("\nPress Esc to retun to the main manu, or any other key to try "
              "again.")
        getchar()
        return "main_menu"
    
    # User Exists & Not already Clocked in - Clock them in
    elif Cur_Entry in Employees:
        _new_clock_in(Cur_Entry)
        print("\nPress Any Key to Return to the Main Menu.")
        getchar()
        return "main_menu"
        # TODO: Add users clock in to time card
       

    # User pressed Escape Key, go back to Main menu
    if Cur_Entry == None or Cur_Entry == '':
        return "main_menu"

SCREENS = {
    "main_menu": main_menu,
    "clock_in": clock_in
}

def main():
    global Screen
    while(True):
        print(Screen)
        next_screen = SCREENS[Screen]()
        if next_screen == "_quit_":
            break
        Screen = next_screen

if __name__ == "__main__":
    main()
