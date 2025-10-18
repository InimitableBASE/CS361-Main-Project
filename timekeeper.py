# Author Justin Holley
# CS361 - Fall 2025

# UI currently works exclusively for windows based systems. 

# Included Libraries
import os



def main_menu():
    os.system('cls') # Clear Screen
    print("\t\t\t\tWELCOME TO TIMEKEEPER!")
    print("\t\tThe Program that tracks your work hours so you can get paid!\n")
    print("MAIN MENU\n")
    print("Select a numerical option from the list below by pressing that "
          "numbers respective key on the keyboard:")
    print("(1)\tClock In")
    print("(2)\tClock Out")
    print("(3)\tSupervisor Menu")
    print("(4)\tQuit")
    print("\n\"Clock In\" tracks when you start work, \"Clock out\" tracks "
          "when you stop work. Each takes less than a minute to help ensure "
          "you are paid for your hard work!")
    print("\nNot sure if you're clocked in or out? Don't worry! You can try "
          "clocking in or clocking out again and the program will tell you if "
          "you are already clocked in or out!")

def clock_in():
    os.system('cls') # Clear Screen
    print("CLOCK IN\n")
    print("Clocking in tracks when you start work.\n")
    print("INSTRUCTIONS:")
    print("To Clock in for work, please enter your Employee ID and Press "
          "Enter.")
    print("\nNot sure if you're clocked in or out? Don't worry! You can try "
        "clocking in or clocking out again and the program will tell you if "
        "you are already clocked in or out!")



def main():
    main_menu()

if __name__ == "__main__":
    main()
