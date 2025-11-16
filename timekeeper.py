# Author Justin Holley
# CS361 - Fall 2025

# UI currently works exclusively for windows based systems. 

# IMPORTED LIBRARIES
import os
import msvcrt
from datetime import datetime
from tabulate import tabulate
from random import randint
import time
import json

# CONSTANT GLOBALS
EMP_FILE = "employees.json"  # eventually store all employee data in JSON
PASSWORD = "123456" # Need to add this password to the program. 

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
Cur_Entry = ''          # tracks the users entries, passed to next screen
Employees = {}          # Dictionary to create employees
Screen = "main_menu"    # Used to specify what screen to go to
Mod_Emp = []            # Tracks modifications to employee in mod emp screeens

# Temporary Globals DELETE WHEN DONE
    # Temporary Employees Dictionary until one exists


"""Function to Load JSON"""
def load_employees(filename):
    global Employees
    with open(filename, "r", encoding='utf-8') as rf:
        Employees = json.load(rf)

def save_employees(filename):
    global Employees
    with open(filename, "w", encoding='utf-8') as wf:
        json.dump(Employees, wf, indent=4)

"""Creates Fake Employees"""
def create_fake_employees():
    global Employees
    Employees['1234'] = {   
        "first": "Elmer",
        "last": "Fudd",
        "wage":  "20.00",
        "clocked_in": False,
        "last_clock_in": None,
        "time_cards": []
    }
    Employees['4567'] = {   
        "first": "Buggs",
        "last": "Bunny",
        "wage":  "25.00",
        "clocked_in": False,
        "last_clock_in": None,
        "time_cards": []
    }
    Employees['7894'] = {   
        "first": "Yosemite",
        "last": "Sam",
        "wage":  "19.00",
        "clocked_in": False,
        "last_clock_in": None,
        "time_cards": []
    }
    return


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

def readTxtFile(file_path):
    """Returns the text from the file at file_path"""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            text = f.read().strip()
            return text
    except FileNotFoundError:
        text = ""
        return text

def writeTxt(file_path, text):
    """Writes the text to the file at file_path"""
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(text)

def useGreetingMS(name):
    # Define folder and file paths
    folder_name = "Greet Folder"
    file_name = "greeting.txt"
    folder_path = os.path.join(os.getcwd(), folder_name)
    file_path = os.path.join(folder_path, file_name)

    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Write name for Greeting Request 
    writeTxt(file_path, name)

    # Get Response
    response = name
    while readTxtFile(file_path) == response:
        continue
    return readTxtFile(file_path)


def _new_clock_in(entry):
    f_name = Employees[entry]['first']
    time = datetime.now().isoformat()
    card = {
            'cit': time, 
            'cot': "",
            'hrs': ""
            }
    Employees[entry]['time_cards'].append(card)
    Employees[entry]['clocked_in'] = True
    Employees[entry]['last_clock_in'] = time
    time = _formatTime(datetime.fromisoformat(time))
    greeting = useGreetingMS(f_name)
    print(greeting)
    print(f'YOU CLOCKED IN AT {time}')
    

def _new_clock_out(entry):
    time = datetime.now().isoformat()        
    f_name = Employees[entry]['first'].upper()
    l_name = Employees[entry]['last'].upper()
    Employees[entry]['time_cards'][-1]['cot'] = time
    Employees[entry]['clocked_in'] = False
    work_duration = datetime.fromisoformat(time) - \
        datetime.fromisoformat(Employees[entry]['time_cards'][-1]['cit'])
    sec_worked = work_duration.total_seconds()
    min_worked = sec_worked / 60
    hrs_worked = sec_worked / 3600
    Employees[entry]['time_cards'][-1]['hrs'] = hrs_worked
    date = _formatDate(datetime.fromisoformat(time))
    time = _formatTime(datetime.fromisoformat(time))
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def generate_eid():
    while True:
        rand_num = ""
        for _ in range(4):
            rand_num += str(randint(0,9))
        if rand_num not in Employees:
            return rand_num 

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
          "when you stop work. Each takes one minute to help ensure "
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
        save_employees(EMP_FILE)
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
    
    # User Exists & Not already Clocked out - Clock them out
    elif Cur_Entry in Employees:
        _new_clock_out(Cur_Entry)
        save_employees(EMP_FILE)
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
    global Cur_Entry     
    Cur_Entry = ''      # Clear Cur_Entry for use in this screen.
    print("VIEW HOURLY EMPLOYEE LIST\n")
    if Employees:
        print("Below is a list of Hourly Employees and their Employee ID\n")
    if not Employees:
        print("EMPLOYEE DATABASE EMPTY")
    else:
        data = [["EMPLOYEE NAME", "EMPLOYEE ID"]]
        for key in Employees:
            name = Employees[key]["first"] + " " + Employees[key]["last"]
            data.append([name, key])
        print(tabulate(data, headers="firstrow", tablefmt="grid", 
                       colalign=("left", "center")))
    
    print("\nINSTRUCTIONS:")
    if not Employees:
        print("Press any key to return to the Supervisor Menu.")
        getchar()
        return "supervisor_menu"
    print("Enter an Employee ID and press Enter to view the Employee's "
          "detailed information.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    

    print("\nPlease enter the Employee ID: ", end="", flush=True)
    Cur_Entry = getentry()

    # User Found, go to details
    if Cur_Entry in Employees:
        return "emp_detail"

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

def employee_detail():
    os.system('cls') # Clear Screen
    global Cur_Entry
    global Mod_Emp
    eid = Cur_Entry
    print("VIEW EMPLOYEE DETAILS\n")
    data = [["EMPLOYEE ID:", eid]]
    data.append(["FIRST NAME:",Employees[eid]["first"]])
    data.append(["LAST NAME:",Employees[eid]["last"]])
    data.append(["HOURLY WAGE:",f"${Employees[eid]["wage"]}"])
    print(tabulate(data, tablefmt="grid", 
                    colalign=("left", "center")))

    print("\nSelect a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    print("(1)\tReturn to Hourly Employee List")
    print("(2)\tModify Hourly Employee")
    print("(3)\tRemove Hourly Employee")   
    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == '\x1b':
            return "supervisor_menu"
        if Cur_Entry == "1":
            return "view_list"
        if Cur_Entry == "2":
            # update globals Cur_Entry and Mod_Emp
            Cur_Entry = eid
            Mod_Emp.append(Employees[eid]["first"])
            Mod_Emp.append(Employees[eid]["last"])
            Mod_Emp.append(Employees[eid]["wage"])
            Mod_Emp.append(eid) 
            return "mod_emp_m"
        if Cur_Entry == "3":
            Cur_Entry = eid
            return "rem_emp_c"       


""" Add Employee Screen (First) """
def add_employee_first():
    os.system('cls')    # Clear Screen
    global Cur_Entry
    Cur_Entry = []      # Clear Cur_Entry for use in this screen.  
    name = ""

    print("ADD HOURLY EMPLOYEE\n")
    print("INSTRUCTIONS:")
    print("Enter the new hourly employee's first name and press Enter.")
    print("To abandon adding the new employeee and return to the Supervisor "
          "Menu, press the Escape key (Esc).")
    
    print("\nEnter the employee's first name: ", end="", flush=True)
    
    name = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if name is None:
        return "supervisor_menu"
    
    # Valid Entry Proceed
    Cur_Entry.append(name)
    return "add_emp_l"
    
""" Add Employee Screen (Last) """
def add_employee_last():
    os.system('cls')    # Clear Screen
    global Cur_Entry
    name = ""

    print("ADD HOURLY EMPLOYEE\n")
    print("INSTRUCTIONS:")
    print("Enter the new hourly employee's last name and press Enter.")
    print("To abandon adding the new employeee and return to the Supervisor "
          "Menu, press the Escape key (Esc).")
    
    print("\nEnter the employee's last name: ", end="", flush=True)
    
    name = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if name is None:
        return "supervisor_menu"
    
    # Valid Entry Proceed
    Cur_Entry.append(name)
    return "add_emp_w"   

""" Add Employee Screen (Wage) """
def add_employee_wage():
    os.system('cls')    # Clear Screen
    global Cur_Entry
    wage = ""

    print("ADD HOURLY EMPLOYEE\n")
    print("INSTRUCTIONS:")
    print("Enter the new hourly employee's wage and press Enter.")
    print("To abandon adding the new employeee and return to the Supervisor "
          "Menu, press the Escape key (Esc).")
    
    print("\nEnter the employee's starting hourly wage: ", end="", flush=True)
    
    wage = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if wage is None:
        return "supervisor_menu"
    
    # remove a leading dollar sign
    if len(wage) > 0 and wage[0] == '$':
        wage = wage[1:]

    # Valid Entry Proceed
    if is_float(wage) and float(wage) > 0:
        Cur_Entry.append(wage)
        eid = generate_eid()
        Cur_Entry.append(eid)
        Employees[eid] = {   
            "first": Cur_Entry[0],
            "last": Cur_Entry[1],
            "wage":  wage,
            "clocked_in": False,
            "last_clock_in": None,
            "time_cards": []
        }
        save_employees(EMP_FILE)
        #####  TODO: ###########
        # TODO: Consider Decimal python library for wages
        #########################
        return "add_emp_c"
    else: 
        print("INVALID ENTRY! Must be a positve number, greater than zero. " 
        "Press any key to try again or press Escape (Esc) to abandon the entry"
        " and go back to the Supervisor Menu.")
        ch = getchar()
        if ch == '\x1b':
            return "supervisor_menu"
        return "add_emp_w"

def add_employee_conf():
    os.system('cls') # Clear Screen
    global Cur_Entry
    global Mod_Emp
    Mod_Emp = []
    first = Cur_Entry[0]
    last = Cur_Entry[1]
    wage = Cur_Entry[2]
    eid = Cur_Entry[3]
    print("ADD HOURLY EMPLOYEE\n")
    print("INSTRUCTIONS:")
    print("\nSelect a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    print(f"\n{first} {last} has been added with a wage of "
          f"${wage}. Their Employee ID is {eid}.\n")
    print("(1)\tReturn to Supervisor Menu")
    print(f"(2)\tUNDO: Remove {first} {last} from hourly "
          "employee list.")
    print(f"(3)\tREDO: Modify the information for {first} {last}")
    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == '\x1b':
            return "supervisor_menu"
        if Cur_Entry == "1":
            return "supervisor_menu"
        if Cur_Entry == "2":
            Cur_Entry = eid
            return "rem_emp_c"
        if Cur_Entry == "3":                                                                        
            # Add first, last, and wage, and EID to Mod_Emp
            Cur_Entry = eid
            Mod_Emp.append(first)
            Mod_Emp.append(last)
            Mod_Emp.append(wage)
            Mod_Emp.append(eid) 
            return "mod_emp_m"        

""" Remove Employee Screen """
def remove_employee():
    os.system('cls')    # Clear Screen
    global Cur_Entry     
    Cur_Entry = ''      # Clear Cur_Entry for use in this screen.
    print("REMOVE HOURLY EMPLOYEE\n")    
    print("INSTRUCTIONS:")
    print("Enter the Employee ID of the hourly employee you'd like to remove "
          "and press Enter.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    
    print("\nPlease enter the Employee ID to remove: ", end="", flush=True)
    
    Cur_Entry = getentry()

    # User Found, go to details
    if Cur_Entry in Employees:
        return "rem_emp_c"                                                     

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
        return "rem_emp"    

"""Remove Employee Confirmation Screen"""
def remove_employee_conf():
    os.system('cls') # Clear Screen
    global Cur_Entry
    eid = Cur_Entry
    print("REMOVE HOURLY EMPLOYEE\n")
    print("INSTRUCTIONS:")
    print("Select a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard.") 
    print("Press the Escape key (Esc) to return to the Supervisor Menu "
          "without removing the employee.\n")
    print("   !!!! WARNING !!!! WARNING !!!! WARNING !!!! WARNING !!!! WARNING"
          " !!!! WARNING !!!! WARNING !!!!")
    print("REMOVING THIS EMPLOYEE WILL PREVENT THEM FROM CLOCKING IN WITH "
          "THEIR EMPLOYEE ID. DATA WILL BE LOST.\n")
    
    print(f"ARE YOU SURE YOU WANT TO PERMANENTLY REMOVE "
          f"{Employees[eid]["first"].upper()} "
          f"{Employees[eid]["last"].upper()} WITH EMPLOYEE ID {eid}?\n")
    print("(1)\tYES - REMOVE EMPLOYEE AND RETURN TO SUPERVISOR MENU")
    print("(2)\tNO - DO NOT REMOVE EMPLOYEE, RETURN TO SUPERVISOR MENU")

    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == '\x1b':
            return "supervisor_menu"
        if Cur_Entry == "1":
            del Employees[eid]
            save_employees(EMP_FILE)
            return "supervisor_menu"
        if Cur_Entry == "2":
            return "supervisor_menu"

""" Modify Employee Screen """
def modify_employee():
    os.system('cls')    # Clear Screen
    global Cur_Entry
    global Mod_Emp     
    Cur_Entry = ''      # Clear Cur_Entry for use in this screen.
    Mod_Emp = []
    print("MODIFY HOURLY EMPLOYEE\n")    
    print("INSTRUCTIONS:")
    print("Enter the Employee ID of the hourly employee you'd like to remove "
          "and press Enter.")
    print("To return to the Supervisor Menu, press the Escape key (Esc).")
    
    print("\nPlease enter the Employee ID to modify: ", end="", flush=True)
    
    Cur_Entry = getentry()

    # User Found, go to details
    if Cur_Entry in Employees:
        # Add first, last, and wage to Mod_Emp
        iter_cnt = 0 
        for val in Employees[Cur_Entry].values():
            if iter_cnt < 3:
                Mod_Emp.append(val)
                iter_cnt += 1
            else:
                break
        Mod_Emp.append(Cur_Entry) # Add EID
        return "mod_emp_m"                                                     

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
        return "mod_emp"    

""" Modify Employee Menu Screen """
def modify_employee_menu():
    os.system('cls') # Clear Screen
    global Mod_Emp
    eid = Mod_Emp[3]

    print("MODIFY HOURLY EMPLOYEE\n")
    
    data = [["EMPLOYEE ID:", Mod_Emp[3]]]
    data.append(["FIRST NAME:",Mod_Emp[0]])
    data.append(["LAST NAME:",Mod_Emp[1]])
    data.append(["HOURLY WAGE:",f"${Mod_Emp[2]}"])
    print(tabulate(data, tablefmt="grid", 
                    colalign=("left", "center")))
    
    print("\nSelect a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard.")
    print("To return to the Supervisor Menu without saving any changes, press "
          "the Escape key (Esc).")
    print("(1)\tModify First Name")
    print("(2)\tModify Last Name")
    print("(3)\tModify Hourly Wage")
    print("(4)\tSave changes and return to Supervisor Menu")   
    while(True):
        Cur_Entry = getchar()
        if Cur_Entry == '\x1b':
            return "supervisor_menu"
        if Cur_Entry == "1":
            return "mod_emp_f"
        if Cur_Entry == "2":
            return "mod_emp_l"
        if Cur_Entry == "3":
            return "mod_emp_w"   
        if Cur_Entry == "4":
            Employees[eid]['first'] = Mod_Emp[0]
            Employees[eid]['last'] = Mod_Emp[1]
            Employees[eid]['wage'] = Mod_Emp[2]
            save_employees(EMP_FILE)
            return "supervisor_menu"   

""" Modiy Employee (First Name) """
def modify_employee_first():
    os.system('cls')    # Clear Screen
    global Mod_Emp
    # Clear Cur_Entry for use in this screen.  
    name = ""

    print("MODIFY HOURLY EMPLOYEE FIRST NAME\n")
    print("INSTRUCTIONS:")
    print("Modify the hourly employee's first name and press Enter.")
    print("press the Escape key (Esc)to go back to the Modify Employee Menu.")
    print(f"\n Current first name: {Mod_Emp[0]}\n")

    print("\nEnter the employee's updated first name: ", end="", flush=True)
    
    name = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if name is None:
        return "mod_emp_m"
    
    # Valid Entry Proceed
    Mod_Emp[0] = name
    return "mod_emp_m"
    
""" Modiy Employee (Last Name) """
def modify_employee_last():
    os.system('cls')    # Clear Screen
    global Mod_Emp
    # Clear Cur_Entry for use in this screen.  
    name = ""

    print("MODIFY HOURLY EMPLOYEE FIRST NAME\n")
    print("INSTRUCTIONS:")
    print("Modify the hourly employee's last name and press Enter.")
    print("press the Escape key (Esc)to go back to the Modify Employee Menu.")
    print(f"\n Current last name: {Mod_Emp[1]}\n")

    print("\nEnter the employee's updated last name: ", end="", flush=True)
    
    name = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if name is None:
        return "mod_emp_m"
    
    # Valid Entry Proceed
    Mod_Emp[1] = name
    return "mod_emp_m"

""" Modiy Employee (wage) """
def modify_employee_wage():
    os.system('cls')    # Clear Screen
    global Mod_Emp
    # Clear Cur_Entry for use in this screen.  
    wage = ""

    print("MODIFY HOURLY EMPLOYEE Wage\n")
    print("INSTRUCTIONS:")
    print("Modify the hourly employee's last name and press Enter.")
    print("press the Escape key (Esc)to go back to the Modify Employee Menu.")
    print(f"\n Current hourly wage for {Mod_Emp[0]} {Mod_Emp[1]}: "
          f"{Mod_Emp[2]}\n")

    print("\nEnter the employee's updated hourly wage: ", end="", flush=True)
    
    wage = getentry()
    
    # User pressed Escape Key, go back to Main menu
    if wage is None:
        return "mod_emp_m"
    
    #####  TODO: ###########
    # TODO: Consider Decimal python library for wages
    #########################

    # remove a leading dollar sign
    if len(wage) > 0 and wage[0] == '$':
        wage = wage[1:]

    # Valid Entry Proceed
    if is_float(wage) and float(wage) > 0:
        Mod_Emp[2] = str(wage)
        return "mod_emp_m"
    else: 
        print("INVALID ENTRY! Must be a positve number, greater than zero. " 
        "Press any key to try again or press Escape (Esc) to go back to the "
        "Modify Employee Menu.")
        ch = getchar()
        if ch == '\x1b':
            return "mod_emp_m"
        return "mod_emp_w"

SCREENS = {
    "main_menu": main_menu,
    "clock_in": clock_in,
    "clock_out": clock_out,
    "supervisor_login": supervisor_login,
    "supervisor_menu": supervisor_menu,
    "sup_help": supervisor_help,
    "view_list": view_employee_list,
    "emp_detail": employee_detail,
    "add_emp": add_employee_first,
    "add_emp_l": add_employee_last,
    "add_emp_w": add_employee_wage,
    "add_emp_c": add_employee_conf,
    "rem_emp": remove_employee,
    "rem_emp_c": remove_employee_conf,
    "mod_emp": modify_employee,
    "mod_emp_m": modify_employee_menu, 
    "mod_emp_f": modify_employee_first,
    "mod_emp_l": modify_employee_last,
    "mod_emp_w": modify_employee_wage
}

def main():
    global Screen
    global EMP_FILE
    if not os.path.exists(EMP_FILE):
        print(f"File: {EMP_FILE} not found.\n")
        print("Creating Fake Employees for testing.")
        create_fake_employees()
        save_employees(EMP_FILE)
        time.sleep(2)
    else:
        load_employees(EMP_FILE)
    while(True):
        print(Screen)
        next_screen = SCREENS[Screen]()
        if next_screen == "_quit_":
            os.system('cls')    # Clear Screen
            break
        Screen = next_screen

if __name__ == "__main__":
    main()
