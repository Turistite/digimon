import RPi.GPIO as gpio
from printingText import *
from mfrc522 import SimpleMFRC522
CardReader = SimpleMFRC522()

def wait_for_a_card():
   printText("Scan a card",2)
   text = CardReader.read()
   print(text[0])
   lcd_clear()
   return text

def try_to_read():
  id, text = CardReader.read_no_block()
  return id;
try:
  # wait_for_a_card()
  while True:
     id = try_to_read() 
     print(id)

finally:
  print("End")
