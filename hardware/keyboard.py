import RPi.GPIO as GPIO
import time

# Set the Row Pins
ROW_1 = 11
ROW_2 = 13
ROW_3 = 15
ROW_4 = 29

# Set the Column Pins
COL_1 = 16
COL_2 = 18
COL_3 = 32
COL_4 = 36

GPIO.setwarnings(False)
# BCM numbering

# Set Row pins as output
GPIO.setup(ROW_1, GPIO.OUT)
GPIO.setup(ROW_2, GPIO.OUT)
GPIO.setup(ROW_3, GPIO.OUT)
GPIO.setup(ROW_4, GPIO.OUT)

# Set column pins as input and Pulled up high by default
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# function to read each row and each column
def readRow(line, characters):
    GPIO.output(line, GPIO.LOW)
    ch = '$'
    if(GPIO.input(COL_1) == GPIO.LOW):
        ch = characters[0]
    if(GPIO.input(COL_2) == GPIO.LOW):
        ch = characters[1]
    if(GPIO.input(COL_3) == GPIO.LOW):
        ch = characters[2]
    if(GPIO.input(COL_4) == GPIO.LOW):
        ch = characters[3]
    GPIO.output(line, GPIO.HIGH)
    return ch

def read_from_keyboard(): 
    while True:
        ch = readRow(ROW_1, ["1","2","3","A"])
        if ch!='$':
            return ch
        ch = readRow(ROW_2, ["4","5","6","B"])
        if ch!='$':
            return ch
        ch = readRow(ROW_3, ["7","8","9","C"])
        if ch!='$':
            return ch
        ch = readRow(ROW_4, ["*","0","#","D"])
        if ch!='$':
            return ch
        time.sleep(0.2) # adjust this per your own setup

