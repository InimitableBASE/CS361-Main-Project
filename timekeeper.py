# Author Justin Holley
# CS361 - Fall 2025

# UI currently works exclusively for windows based systems. 

# IMPORTED LIBRARIES
import os
import msvcrt

# Temporary Globals
USER1ID = '1234'

# GLOBALS
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
CurrentEntry = ''      # Used to track the users current entry

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
        if ord(ch) == 27:
            return          
        
        # If Entry is Backspace
        if ord(ch) == 8:
            if len(entry) > 0:
                entry = entry[:-1] # remove last character
                # move cursor back, print space over it, move cursor back again
                print("\b \b", end="", flush=True) 

        # if the character is printable, add it to the CurrentEntry
        if ch.isprintable():
            entry += ch
            print(f'{ch}', end="", flush=True)

        # if Entry is Enter
        if ord(ch) == 13:
            print("", end="\n", flush=False)
            return entry           


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
    CurrentEntry = getchar()
    if CurrentEntry == "1":
        clock_in()        



def clock_in():
    os.system('cls')    # Clear Screen
    CurrentEntry = ''   # Clear CurrentEntry for use in this screen.  
    
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
    CurrentEntry = getentry()

    # User Exists - Clock them in
    if CurrentEntry == USER1ID:
        print("\nFIRST LAST CLOCKED IN AT TIME")
        # TODO: Add users clock in to time card

    # User pressed Escape Key, go back to Main menu
    if CurrentEntry == None:
        # TODO: Handle State change
        pass
        

def main():
    main_menu()

if __name__ == "__main__":
    main()
