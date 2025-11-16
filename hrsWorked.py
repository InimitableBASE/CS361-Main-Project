import json
from datetime import datetime
from time import sleep

def loadJson(path):
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def readTxtFile(file_path):
    """Returns the text from the file at file_path"""
    try:
        with open(file_path, "r") as f:
            text = f.read().strip()
            return text
    except FileNotFoundError:
        text = ""
        return text
    
def writeHoursTxt(file_path, text):
    """Writes the hours worked to the file at file_path"""
    with open(file_path, "w") as f:
        f.write(text)

def main():
    """Main Program loop"""
    ### Setup text file, create if not present
    
    # Set Folder Name
    file_path = "workhours.txt"
    
    # Ensure workhours.txt file exists, create blank workhours.txt file
    with open(file_path, "w") as f:
        f.write("")

    # stores the last text read/written by the program to the file at filepath
    last_text = ""

    # System Message
    print(f"Watching '{file_path}' for updates...")
    
    # Main Loop for processing requests
    while True:
        displayMin = False
        
        # Read greeting.txt file
        text = readTxtFile(file_path)

        # Is text not blank and different from previously read text
        if text and text != last_text:
            
            eid = text
            
            # check if eid is valid and has 'm' appended.
            if len(eid) == 5 and eid[-1] == 'm':
                eid = eid[:-1]
                displayMin = True
            elif len(eid) != 4:
                writeHoursTxt(file_path, "ERROR: INVALID EID OR COMMAND")
                last_text = "ERROR: INVALID EID OR COMMAND"
                continue
        
            # load json
            employees = loadJson('employees.json')
            
            if eid not in employees:
                writeHoursTxt(file_path, "ERROR: INVALID EID OR COMMAND")
                last_text = "ERROR: INVALID EID OR COMMAND"
                continue

            # employee record
            emp = employees[eid]
            # get employee full name
            name = emp['first'] + " " +  emp['last']

            # initialize hrsWorked to zero
            hrsWorked = 0

            # get current time if emp is clocked in so hours worked includes
            # current hours worked as well. 
            if emp["clocked_in"]:
                now = datetime.now()
            
            # loop employee through timecards, sum hours 
            for timeCard in emp["time_cards"]:
                if timeCard["hrs"] != "":
                    hrsWorked += timeCard["hrs"]
                else:       # Employee clocked in
                    cit = datetime.fromisoformat(timeCard["cit"])
                    deltaHrs = now - cit
                    deltaHrs = deltaHrs.total_seconds()
                    deltaHrs /= 3600
                    hrsWorked += deltaHrs

            if displayMin:         # if user wants to display minutes
                min = hrsWorked - int(hrsWorked)
                min = min * 60
                ihrsWorked = int(hrsWorked)
                imin = int(min)
                # Handle proper english repsonse
                if ihrsWorked == 0:
                    if imin == 0: 
                        response = f"0 Hours"
                    elif imin == 1:
                        response = f"1 minute"
                    else:
                        response = f"{imin} minutes"
                elif ihrsWorked == 1:
                    if imin == 0: 
                        response = f"0 Minutes"
                    elif imin == 1:
                        response = f"1 minute"
                    else:
                        response = f"1 hour {imin} minutes"
                else:
                    if imin == 0: 
                        response = f"{ihrsWorked} hours 0 Minutes"
                    elif imin == 1:
                        response = f"{ihrsWorked} hours 1 minute"
                    else:
                        response = f"{ihrsWorked} hours {imin} minutes"
            else:   # User only wants string of hours worked
                response = f"{hrsWorked}"
            
            print(f"Writing: {response}")
            writeHoursTxt(file_path, response)
            # set last_text to response. 
            last_text = response
            print("\nWatching 'workhours.txt' for updates...")
        sleep(1)  # small delay to lower resource usage

if __name__ == "__main__":
    main()