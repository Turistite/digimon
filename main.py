players
current_player = 0
nfc_id_auction

import time

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5

def await_end_of_turn():
	print("await_end_of_turn")

def read_nfc_card():
	print("read_nfc_card")

def try_read_nfc_card():
	print("try_read_nfc_card")

def display_on_screen(text):
	print("display_on_screen")

def auction():
	value = 100 //NASKO
	value = COEF_AUCTION*value
	step = COEF_STEP*value
	start = time.time()
	current_owner = null

	while time.time()<=(start+5):
		display_on_screen(value)
		id = try_read_nfc_card()
	    if id!=null:
			current_owner = get_player_by_id(id) //NASKO
			start = time.time()
			time.sleep(1)
			value += step


	if current_owner!=null:
		current_owner.buy();

	print("auction")

def buy():
	current_player.pay()
	current_field.owner = current_player;

def process_turn(status):
	if status==N:
		await_end_of_turn()
	elif status==P:
		current_player.pay()
		await_end_of_turn()
	elif status==T:
		id = read_nfc_card()
		if id==nfc_id_auction:
			auction()
		elif (id==current_player.id):
			current_player.buy()
		else:
			print("Error")
			//TBD retry read_nfc_card


while True:
	moves = inputFromKeyboard()
	state = current_player.roll_dice(moves)
	process_turn(state)
