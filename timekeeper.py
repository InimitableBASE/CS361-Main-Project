# Author Justin Holley
# CS361 - Fall 2025

# UI currently works exclusively for windows based systems. 

# IMPORTED LIBRARIES
import os
import msvcrt
from datetime import datetime
from tabulate import tabulate
import time

# GLOBALS
EMP_FILE = "employees.json"  # eventually store all employee data in JSON
PASSWORD = "123"

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

        # if the character is printable, add it to the entry
        if ch.isprintable():
            entry += ch
            print(f'{ch}', end="", flush=True)

        # if entry is Enter
        if ch == '\r':
            print("", end="\n", flush=False)
            return entry           

"""
Function that gets a users password input and returns it when they press enter. 
If the user presses Escape, program returns without returning an entry. 
Password is visually hidden during entry.
"""
def getpassword():
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

        # if the character is printable, add it to the entry
        if ch.isprintable():
            entry += ch
            print("*", end="", flush=True)

        # if entry is Enter
        if ch == '\r':
            print("", end="\n", flush=False)
            return entry         

# HELPER FUNCTIONS
def _formatTime(time):
    return time.strftime('%H:%M:%S')

def _formatDate(time):
    return time.strftime('%m/%d/%Y')

def _new_clock_in(entry):
    f_name = Employees[entry]['first'].upper()
    l_name = Employees[entry]['last'].upper()
    time = datetime.now()
    card = {
            'cit': time, 
            'cot': "",
            'hrs': ""
            }
    Employees[entry]['time_cards'].append(card)
    Employees[entry]['clocked_in'] = True
    Employees[entry]['last_clock_in'] = time
    date = _formatDate(time)
    time = _formatTime(time)
    # time = Employees[Cur_Entry]['time_cards'][-1]['cit']
    print(f'\n{f_name} {l_name} HAS CLOCKED IN ON {date} AT {time}')

def _new_clock_out(entry):
    time = datetime.now()        
    f_name = Employees[entry]['first'].upper()
    l_name = Employees[entry]['last'].upper()
    Employees[entry]['time_cards'][-1]['cot'] = time
    Employees[entry]['clocked_in'] = False
    work_duration = time - Employees[entry]['time_cards'][-1]['cit']
    sec_worked = work_duration.total_seconds()
    min_worked = sec_worked / 60
    hrs_worked = sec_worked / 3600
    Employees[entry]['time_cards'][-1]['hrs'] = hrs_worked
    date = _formatDate(time)
    time = _formatTime(time)
    if hrs_worked < 1:
        print(
            f"\n{f_name} {l_name} WORKED {min_worked:.1f} MINUTES AND CLOCKED "
            f"OUT ON {date} AT {time}"
            )   
    else:
        print(
            f"\n{f_name} {l_name} WORKED {hrs_worked} HOURS AND CLOCKED OUT ON"
            f" {date} AT {time}"
            )


"""Main Menu Screen"""
def main_menu():
    os.system('cls') # Clear Screen
    print("\t\t\t\tWELCOME TO TIMEKEEPER!")
    print("\t\tThe program that tracks your work hours so you can get paid!\n")
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
        if Cur_Entry == "2":
            return "clock_out"
        if Cur_Entry == "3":
            return "supervisor_login"       
        if Cur_Entry == "4":
            return "_quit_"

""" Clock In Screen """
def clock_in():
    os.system('cls')    # Clear Screen
    Cur_Entry = ''   # Clear Cur_Entry for use in this screen.  
    
    print("CLOCK IN\n")
    print("Clocking in tracks when you start work.\n")
    print("INSTRUCTIONS:")
    print("To clock in for work, please enter your Employee ID and press "
          "Enter.")
    print("To return to the Main Menu, press the Escape key (Esc).")
    print("\nNot sure if you're clocked in? Don't worry! You can try clocking "
          "in and the program will tell you if you are already clocked in!")
    
    print("\nPlease enter your Employee ID: ", end="", flush=True)
    
    Cur_Entry = getentry()

    # User Exists and is already clocked in
    if Cur_Entry in Employees and Employees[Cur_Entry]["clocked_in"]:
        f_name = Employees[Cur_Entry]['first'].upper()
        l_name = Employees[Cur_Entry]['last'].upper()
        print(f'\n{f_name} {l_name} IS ALREADY CLOCKED IN!')
        print("\nPress the Escape key (Esc) to return to the Main Menu, or "
              "any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "main_menu"
        return "clock_in"
    
    # User Exists & Not already Clocked in - Clock them in
    elif Cur_Entry in Employees:
        _new_clock_in(Cur_Entry)
        print("\nPress any key to return to the Main Menu.")
        getchar()
        return "main_menu"

    # User pressed Escape Key, go back to Main menu
    if Cur_Entry == None:
        return "main_menu"
    
    # Invalid Entry
    if Cur_Entry not in Employees:
        print("\nThat is not a valid Employee ID. See a Supervisor "
              "if you have forgotten your Employee ID.")
        print("\nPress the Escape key (Esc) to return to the Main Menu, or "
              "any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "main_menu"
        return "clock_in"    

""" Clock Out Screen """
def clock_out():
    os.system('cls')    # Clear Screen
    Cur_Entry = ''   # Clear Cur_Entry for use in this screen.  
    
    print("CLOCK OUT\n")
    print("Clocking out tracks when you stop work.\n")
    print("INSTRUCTIONS:")
    print("To clock out from work, please enter your Employee ID and press "
          "Enter.")
    print("To return to the Main Menu, press the Escape key (Esc).")
    print("\nNot sure if you're clocked out? Don't worry! You can try clocking"
          " out again and the program will tell you if you are already "
          "clocked out!")
    
    print("\nPlease enter your Employee ID: ", end="", flush=True)
    
    Cur_Entry = getentry()

    # User Exists and is already clocked out
    if Cur_Entry in Employees and not Employees[Cur_Entry]["clocked_in"]:
        f_name = Employees[Cur_Entry]['first'].upper()
        l_name = Employees[Cur_Entry]['last'].upper()
        print(f'\n{f_name} {l_name} IS ALREADY CLOCKED OUT!') 
        print("\nYou must clock in before you may clock out. If you forgot to "
              "clock in for work, see a Supervisor.")
        print("\nPress the Escape key (Esc) to return to the Main Menu, or "
              "any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "main_menu"
        return "clock_out"
    
    # User Exists & Not already Clocked in - Clock them in
    elif Cur_Entry in Employees:
        _new_clock_out(Cur_Entry)
        print("\nPress any key to return to the Main Menu.")
        getchar()
        return "main_menu"

    # User pressed Escape Key, go back to Main menu
    if Cur_Entry == None:
        return "main_menu"
    
    # Invalid Entry
    if Cur_Entry not in Employees:
        print("\nThat is not a valid Employee ID. See a Supervisor "
              "if you have forgotten your Employee ID.")
        print("\nPress the Escape key (Esc) to return to the Main Menu, or "
              "any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "main_menu"
        return "clock_out"    

""" Supervisor Login Screen """
def supervisor_login():
    os.system('cls')    # Clear Screen
    Cur_Entry = ''   # Clear Cur_Entry for use in this screen.  
    
    print("SUPERVISOR LOGIN\n")
    print("INSTRUCTIONS:")
    print("To access the Supervisor Menu, please enter the supervisor password"
          " press Enter.")
    print("To return to the Main Menu, press the Escape key (Esc).")
    
    print("\nSupervisor Password: ", end="", flush=True)
    
    Cur_Entry = getpassword()
    
    # User Exists & Not already Clocked in - Clock them in
    if Cur_Entry == PASSWORD:
        return "supervisor_menu"

    # User pressed Escape Key, go back to Main menu
    if Cur_Entry == None:
        return "main_menu"
    
    # Invalid Entry
    if Cur_Entry != PASSWORD:
        print("\nINCORRECT PASSWORD")
        print("\nPress the Escape key (Esc) to return to the Main Menu, or "
              "any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "main_menu"
        return "supervisor_login"    

def supervisor_menu():
    os.system('cls') # Clear Screen
    print("SUPERVISOR MENU\n")
    print("Select a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard.")
    print("To return to the Main Menu, press the Escape key (Esc).")
    print("(1)\tView Hourly Employee List")
    print("(2)\tAdd Hourly Employee")
    print("(3)\tModify Hourly Employee")
    print("(4)\tRemove Hourly Employee")
    print("(5)\tView Supervisor Help Menu")
    print("(6)\tLogout and Return to Main Menu")    
    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == '\x1b':
            return "main_menu"
        if Cur_Entry == "1":
            return "view_list"
        if Cur_Entry == "2":
            return "add_emp"
        if Cur_Entry == "3":
            return "mod_emp"       
        if Cur_Entry == "4":
            return "rem_emp"
        if Cur_Entry == "5":
            return "sup_help"       
        if Cur_Entry == "6":
            return "main_menu"

def supervisor_help():
    os.system('cls') # Clear Screen
    print("SUPERVISOR MENU HELP")
    print("\nTo return to the Supervisor Menu, press any key.\n")
    message = """TO VIEW EMPLOYEE INFORMATION AND MODIFY OR REMOVE THEM: 
To view the Employee List, Press the “1” key at the Supervisor Menu. This 
will display a list of Hourly Employees and their Employee ID. Enter an 
Employee ID and press the Enter key to see details about that Employee. To 
Modify that Employee's Information press the “2” Key. To Remove that Employee, 
press the “3” Key."""
    print(message)
    message = """\nADD A NEW EMPLOYEE:\nPress the “2” key at the Supervisor
Menu to Add a new Employee. Enter the information that is prompted (First Name,
Last Name, and Hourly Wage) and press the Enter key after each entry."""
    print(message)
    print("\nPress any key to return to the Main Menu.")
    getchar()
    return "supervisor_menu"

""" View Hourly Employee List Screen """
def view_employee_list():
    os.system('cls')    # Clear Screen
    Cur_Entry = ''   # Clear Cur_Entry for use in this screen.  
    
    print("VIEW HOURLY EMPLOYEE LIST\n")
    print("Below is a list of Hourly Employees and their Employee ID\n")
    
# Employees['1234'] = {   
#     "first": "Elmer",
#     "last": "Fudd",
#     "wage":  "20.00",


    if not Employees:
        print("EMPLOYEE DATABASE EMPTY")
    else:
        # print("NAME: EMPLOYEE ID")
        data = [["EMPLOYEE NAME", "EMPLOYEE ID"]]
        for key in Employees:
            name = Employees[key]["first"] + " " + Employees[key]["last"]
            data.append([name, key])
            # print(f'{Employees[key]["first"]}', end="")
            # print(f' {Employees[key]["last"]}:', end="")
            # print(f' {key}', end="\n")
        print(tabulate(data, headers="firstrow", tablefmt="grid", 
                       colalign=("left", "center")))
    
    print("\nINSTRUCTIONS:")
    print("Enter an Employee ID and press Enter to view the Employee's "
          "detailed information.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    
    print("\nPlease enter the Employee ID: ", end="", flush=True)
    
    Cur_Entry = getentry()

    # User Exists and is already clocked out
    if Cur_Entry in Employees:
        print("UNDER CONSTRUCTION")
        time.sleep(3)
        return "supervisor_menu"

    # User pressed Escape Key, go back to Supervisor menu
    if Cur_Entry == None:
        return "supervisor_menu"
    
    # Invalid Entry
    if Cur_Entry not in Employees:
        print("\nThat is not a valid Employee ID.")
        print("\nPress the Escape key (Esc) to return to the Supervisor Menu, "
              "or any other key to try again.")
        ch = getchar()
        if ch == '\x1b':
            return "supervisor_menu"
        return "view_list"    

SCREENS = {
    "main_menu": main_menu,
    "clock_in": clock_in,
    "clock_out": clock_out,
    "supervisor_login": supervisor_login,
    "supervisor_menu": supervisor_menu,
    "sup_help": supervisor_help,
    "view_list": view_employee_list
}



def main():
    global Screen
    while(True):
        print(Screen)
        next_screen = SCREENS[Screen]()
        if next_screen == "_quit_":
            os.system('cls')    # Clear Screen
            break
        Screen = next_screen

if __name__ == "__main__":
    main()
