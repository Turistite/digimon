import time
import RPi.GPIO as gpio
from hardware.lcdScreen import *
from mfrc522 import SimpleMFRC522
CardReader = SimpleMFRC522()

def wait_for_a_card():
   text = CardReader.read()
   print(text[0])
   time.sleep(2)
   lcd_clear()
   return text[0]

def try_to_read():
  id, text = CardReader.read_no_block()
  return id;
