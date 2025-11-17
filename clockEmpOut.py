import json
from datetime import datetime
from time import sleep

def loadJson(path):
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def save_employees(filename, employees):
    global Employees
    with open(filename, "w", encoding='utf-8') as wf:
        json.dump(employees, wf, indent=4)

def readTxtFile(file_path):
    """Returns the text from the file at file_path"""
    try:
        with open(file_path, "r") as f:
            text = f.read().strip()
            return text
    except FileNotFoundError:
        text = ""
        return text
    
def writeTxtFile(file_path, text):
    """Writes the hours worked to the file at file_path"""
    with open(file_path, "w") as f:
        f.write(text)

def eidInEmployees(eid):
    employees = loadJson('employees.json')
    if eid in employees:
        return True
    else:
        return False 
    
def clockOutEmp(eid):
    # get time
    time = datetime.now().isoformat()
    
    # load employees data structure      
    employees = loadJson('employees.json')
    
    f_name = employees[eid]['first'].upper()
    l_name = employees[eid]['last'].upper()

    if not employees[eid]["clocked_in"]:
        response = f"{f_name} {l_name} already clocked out!"
        return response


    # set clockout time
    employees[eid]['time_cards'][-1]['cot'] = time
    
    # set clocked in status to False
    employees[eid]['clocked_in'] = False
    
    # calculate hours worked
    work_duration = datetime.fromisoformat(time) - \
        datetime.fromisoformat(employees[eid]['time_cards'][-1]['cit'])
    sec_worked = work_duration.total_seconds()
    hrs_worked = sec_worked / 3600
    employees[eid]['time_cards'][-1]['hrs'] = hrs_worked
    
    # save employees.json
    save_employees("employees.json", employees)

    response = f"{f_name} {l_name} is now clocked out."
    
    return response

def clockOutAll():
    # load employees data structure      
    employees = loadJson('employees.json')
    for eid in employees:
        if employees[eid]["clocked_in"]:
            clockOutEmp(eid)
    return "All employees clocked out."
            
def getName(eid):
    # load employees data structure      
    employees = loadJson('employees.json')
    return employees[eid]['first'] + " " + employees[eid]['last'] 



def main():
    """Main Program loop"""
    ### Setup text file, create if not present
    
    # Set Folder Name
    file_path = "clockout.txt"
    
    # Ensure clockout.txt file exists, create blank workhours.txt file
    with open(file_path, "w") as f:
        f.write("")

    # stores the last text read/written by the program to the file at filepath
    last_text = ""

    # System Message
    print(f"Watching '{file_path}' for updates...")
    
    # Main Loop for processing requests
    while True:        
        # Read greeting.txt file
        text = readTxtFile(file_path)

        # Is text not blank and different from previously read text
        if text and text != last_text:
            
            # check if text is letters, make lowercase if so. 
            if text.isalpha():
                text = text.lower()

            # check if text is valid entry
            if len(text) != 4 and text !="all":
                writeTxtFile(file_path, "ERROR: INVALID EID OR COMMAND")
                last_text = "ERROR: INVALID EID OR COMMAND"
                continue

            if text == "all":
                response = clockOutAll()
                
            else:
                eidInEmployees(text)
                response = clockOutEmp(text)
            
            print(f"Writing: {response}")
            writeTxtFile(file_path, response)
            # set last_text to response. 
            last_text = response
            print("\nWatching 'workhours.txt' for updates...")
        sleep(1)  # small delay to lower resource usage

if __name__ == "__main__":
    main()