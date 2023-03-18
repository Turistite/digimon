from game.game_state import *
from hardware.CardRead import *
import time

nfc_id_auction = 633367768675

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5

def await_end_of_turn():
	print("await_end_of_turn")
	#TODO button

def read_nfc_card():
	print("read_nfc_card")

def get_player_by_id(id):
	return id
	
def try_read_nfc_card():
	print("try_read_nfc_card")

def display_on_screen(text):
	print("display_on_screen")

def auction():
	value = gameState.fields[gameState.players[gameState.curr_player].position].price
	value = int(COEF_AUCTION*value)
	step = int(COEF_STEP*value)
	start = time.time()
	current_owner = -1

	while time.time()<=(start+5):
		printText(value,1)
		id = try_read_nfc_card()
		if id!=-1:
			lcd_clear()
			current_owner = get_player_by_id(id)
			start = time.time()
			time.sleep(1)
			value += step


	if current_owner!=-1:
		#TODO buy with specific value
		printText("Successfully bought for " + value, 1)
		time.sleep(1.5)

	print("auction")

def buy():
	gameState.players[gameState.curr_player].buy(gameState.players[gameState.curr_player].position)

def process_turn(status):
	if status==Action.NOTHING:
		await_end_of_turn()
	elif status==Action.PAYMENT:
		buy()
		await_end_of_turn()
	elif status==Action.PENDING:
		id = wait_for_a_card()
		if id == nfc_id_auction:
			auction()
		elif (id==gameState.players[gameState.curr_player]):
			buy()
		else:
			print("Error")
			#TBD retry read_nfc_card

def players_id():
    printText("Number of players:",1)
    #num_players = inputFromKeyboard()
    num_players = 4
    time.sleep(3)
    lcd_clear()
    list_id = []
    for i in range(num_players):
      printText("Scan player " + str(i+1) + " card", 2)
      time.sleep(1.5)
      curr_id = wait_for_a_card()
      list_id.append(curr_id)
      print(list_id)
      lcd_clear()
    return list_id


players_ID = players_id()
gameState = GameState(players_ID)

while True:
   #moves = inputFromKeyboard()
   moves = 5
   state = gameState.dice(moves)
   process_turn(state)
