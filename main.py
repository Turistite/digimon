from game.game_state import *
from hardware.CardRead import *
import time

nfc_id_auction = 633367768675

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5
wait_const = 1.0
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
	print("auction")
	value = gameState.fields[gameState.players[gameState.curr_player].position].price
	value = int(COEF_AUCTION*value)
	step = int(COEF_STEP*value)
	start = time.time()
	current_owner = -1
	printText("Auction mode", 1)
	printText("Current price:" + str(value), 2)
	while time.time()<=(start+5):
		printText("Current price:" + str(value), 2)
		id = try_read_nfc_card()
		if id!=-1:
			current_owner = get_player_by_id(id)
			start = time.time()
			time.sleep(1)
			value += step


	if current_owner!=-1:
		lcd_clear()
		#TODO buy with specific value
		printText("Successfully bought for " + value, 1)
		time.sleep(1.5)
		lcd_clear()

	

def buy():
	gameState.players[gameState.curr_player].buy(gameState.players[gameState.curr_player].position)

def process_turn(status):
	if status==Action.NOTHING:
		await_end_of_turn()
	elif status==Action.PAYMENT:
		printText("Transaction:", 1)
		printText(gameState.players[gameState.curr_player].color.name + " --> " + gameState.fields[gameState.players[gameState.curr_player].position].owner.name , 2)
		printText("Amount: " + str(gameState.fields[gameState.players[gameState.curr_player].position].get_rent()), 3)
		gameState.players[gameState.curr_player].pay(gameState.fields[gameState.players[gameState.curr_player].position].owner, gameState.fields[gameState.players[gameState.curr_player].position].get_rent())
		await_end_of_turn()
		time.sleep(wait_const)
		lcd_clear()

	elif status==Action.PENDING:
		printText("Scan a card to buy", 1)
		printText("or two enter auction mode", 2)
		id = wait_for_a_card()
		lcd_clear()
		if id == nfc_id_auction:
			auction()
		elif (id==gameState.players[gameState.curr_player]):
			printText("Successfully bought" , 2)
			time.sleep(wait_const)
			lcd_clear()
			buy()
		else:
			print("Error")
			#TBD retry read_nfc_card

def players_id():
    printText("Number of players:",1)
    #num_players = inputFromKeyboard()
    num_players = 4
    lcd_clear()
    list_id = []
    for i in range(num_players):
      printText("Scan " + str(i) + "th player card")
      curr_id = wait_for_a_card()
      list_id.append(curr_id)
      lcd_clear()
      time.sleep(1.5)
    
    printText("Loading.", 2)
    time.sleep(0.5)
    printText("Loading..", 2)
    time.sleep(0.5)
    printText("Loading...", 2)
    time.sleep(0.5)
    lcd_clear()
    
    return list_id

def inputMoves():
	printText("Enter first dice:",2)
	dice1 = input_from_keyboard()
	printText("First dice: " + str(dice1), 2)
	printText("Enter second dice:", 3)
	dice2 = input_from_keyboard()
	printText("Second dice: " + str(dice2), 3)
	time.sleep(1)
	lcd_clear()
	return (dice1,dice2)
	
players_ID = players_id()
gameState = GameState(players_ID)

while True:
   dices = inputMoves()
   state = gameState.dice(dices)
   process_turn(state)
