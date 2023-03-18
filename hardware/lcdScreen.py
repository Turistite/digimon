import hardware.drivers as drivers
from time import sleep
from datetime import datetime

display = drivers.Lcd()

def centralizedText(text):
   center = int((20 - len(text))/2)
   for i in range (center):
    text = " " + text
   return text
def printText(text,row):
   display.lcd_display_string( centralizedText(text),row)
def lcd_clear():
   display.lcd_clear()
