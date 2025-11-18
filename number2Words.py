from time import sleep

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

def _helperConvert(n, values, words):
    output = ""
    
    # Iterating over all key Numeric values
    for i in range(len(values)):
        value = values[i]
        word = words[i]

        # If the number is greater than or equal to the current numeric value
        if n >= value:

            # Append the quotient part
            # If the number is greater than or equal to 100
            # then only we need to handle that
            if n >= 100:
                output += _helperConvert(n // value, values, words) + " "

            # Append the word for numeric value
            output += word

            # Append the remainder part
            if n % value > 0:
                output += " " + _helperConvert(n % value, values, words)

            return output

    return output

def convertToWords(n):
    if n == 0:
        return "Zero"

    # Key Numeric values and their corresponding English words
    values = [1000000000, 1000000, 1000, 100, 90, 80, 70, 
              60, 50, 40, 30, 20, 19, 18, 17, 16, 15, 14,
              13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    words = ["Billion", "Million", "Thousand", "Hundred", 
             "Ninety", "Eighty", "Seventy", "Sixty", "Fifty",
             "Forty", "Thirty", "Twenty", "Nineteen",
             "Eighteen", "Seventeen", "Sixteen", "Fifteen",
             "Fourteen", "Thirteen", "Twelve", "Eleven",
             "Ten", "Nine", "Eight", "Seven", "Six", "Five",
             "Four", "Three", "Two", "One"]
  
    return _helperConvert(n, values, words)

def isDollar(text: str):
    if text[0] != '$':
        return False
    if text[-3] != '.':
        return False
    if len(text) == 4 and text[1] != '.':
        return False
    if not text[-2:].isnumeric():
        return False
    if len(text) > 4 and not text[1:-3].isnumeric():
        return False
    return True
    
def getValues(text):
    text = text[1:]
    if len(text) == 3:
        dollar = 0
    else: 
        dollar = int(text[:-3])
    cents = int(text[-2:])
    return [dollar, cents]




def main():
    """Main Program loop"""
    ### Setup text file, create if not present
    
    # Set Folder Name
    file_path = "convertnumber.txt"
    
    # Ensure clockout.txt file exists, create blank workhours.txt file
    with open(file_path, "w") as f:
        f.write("")

    # stores the last text read/written by the program to the file at filepath
    last_text = ""

    # System Message
    print(f"Watching '{file_path}' for updates...")

    # Main Loop for processing requests
    while True:        
        # Read file
        text = readTxtFile(file_path)

        # Is text not blank and different from previously read text
        if text and text != last_text:
            
            # check if text is letters, make lowercase if so. 
            if text.isalpha():
                text = text.lower()

            currencyVal = isDollar(text)
            positiveInt = text.isdigit()

            # check if text is valid entry
            if not currencyVal and not positiveInt:
                writeTxtFile(file_path, "ERROR: INVALID ENTRY")
                last_text = "ERROR: INVALID ENTRY"
                continue
            
            if currencyVal:
                dollars, cents = getValues(text)
                dollars = convertToWords(dollars)
                cents = convertToWords(cents)
                response = f"{dollars} dollars and {cents} cents"
            elif positiveInt:
                response = convertToWords(int(text))

            print(f"Writing: {response}")
            writeTxtFile(file_path, response)
            # set last_text to response. 
            last_text = response
            print("\nWatching 'convertnumber.txt' for updates...")
        sleep(1)  # small delay to lower resource usage


if __name__ == "__main__":
    main()
