from game.game_state import GameState
from game.utils.enums import Action
from hardware.CardRead import *
from hardware.keyboard import *
import time

nfc_id_auction = 633367768675

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5

def print_cell_info():
    print (gameState.fields[gameState.players[gameState.curr_player].position])
    
def print_info():
    for player in gameState.players:
        print (str(player.color) + str(player.balance))
    
def await_end_of_turn():
    print_info()
    lcd_clear()
    printText("0 to see balance",1)
    printText("* to upgrade",2)
    printText("A/B to mortgage",3)
    printText("any other to end",4)
    key =  read_from_keyboard()
    if key=='0':
        lcd_clear()
        printText("Your balance is: ",2)
        printText(str(gameState.players[gameState.curr_player].balance),3)
        time.sleep(3)
        lcd_clear()
        await_end_of_turn()
    elif key == "*":
        print("")
        # unknown
        # TODO  upgrade_property(
        await_end_of_turn()
    elif key == "A":
        print("")
        # TODO mortgage

    elif key == "B":
        print("")
        # TODO immortgage
    else:
        return 
#TODO Eventually other turns

def read_nfc_card():
    print("read_nfc_card")

def auction():

    lcd_clear()
    print("Enter auction function")
    printText("--Auction--",1)
    value = gameState.fields[gameState.players[gameState.curr_player].position].price
    value = int(COEF_AUCTION*value)
    field = gameState.fields[gameState.players[gameState.curr_player].position]
    step = int(COEF_STEP*value)
    current_owner = False

    wait=0
    while wait<5:
        wait+=1
        printText("Current price:",2)
        printText(str(value), 3)
        id = try_to_read()
        if id:
            lcd_clear()
            print(id)
            current_owner = gameState.get_player_by_id(id)
            start = time.time()
            #time.sleep(1)
            value += step
            wait=0
        time.sleep(1)

    if current_owner:
        current_owner.buy(field,value)
        printText("Successfully bought for " + str(value), 1)
        time.sleep(1.5)
        lcd_clear()

    await_end_of_turn()


def buy():
    print("Enter buy function")
    gameState.players[gameState.curr_player].buy(
        gameState.fields[gameState.players[gameState.curr_player].position]
    )


def process_turn(status):
    curr_player = gameState.get_current_player()
    curr_field = gameState.fields[curr_player.position]
    die = 1 # TODO

    if status == Action.NOTHING:
        await_end_of_turn()
    elif status == Action.PAYMENT:
        printText("Pay rent: " + str(curr_field.get_rent(die)), 2)
        id = wait_for_a_card()
        while id != gameState.players[gameState.curr_player].id:
            printText("Invalid card!", 3)
            id = wait_for_a_card()
        curr_player.pay(curr_field.get_rent(die), curr_field.owner)
        lcd_clear()
        printText("Rent successfully paid", 2)
        time.sleep(2)
        lcd_clear()
        await_end_of_turn()
    elif status == Action.PENDING:
        print("pending action")
        printText("Buy or start auction", 2)
        id = wait_for_a_card()
        if id == nfc_id_auction:
            time.sleep(1)
            auction()
        elif (id == gameState.players[gameState.curr_player].id):
            printText("Successfully bought", 2)
            time.sleep(1.5)
            lcd_clear()
            buy()
            await_end_of_turn()
        else:
            printText("Card not valid",2)
            process_turn(status)
            # TBD retry read_nfc_card



def players_id():
    printText("Number of players:", 1)
    num_players = read_from_keyboard()
    while num_players < "1" or num_players > "6":
        printText("Enter the number of the players again", 2)
        num_players = read_from_keyboard()
    players_count = int(num_players)
    lcd_clear()
    printText("Numbers of players: " + num_players, 1)
    time.sleep(1)
    lcd_clear()
    list_id = []
    printText("Scan player " + str(1) + " card", 2)
    for i in range(players_count):
        curr_id = wait_for_a_card()
        lcd_clear()
        if i+2 <= players_count:
            printText("Scan player " + str(i+2) + " card", 2)
        time.sleep(1)
        list_id.append(curr_id)
        print(list_id)
    return list_id


def proccess_action():
    # TODO stuff
    # proccessing functions
    print("Something")


players_ID = players_id()
gameState = GameState(players_ID)

while True:
    printText("Enter what dices have been thrown!", 1)
    time.sleep(2)
    lcd_clear()
    printText("player " + str(gameState.curr_player+1), 1)
    printText("Dice one:", 2)
    moves = [0, 0]
    moves[0] = read_from_keyboard()
    while moves[0] < "1" or moves[0] > "6":
        moves[0] = read_from_keyboard()
        lcd_clear()
        printText("player " + str(gameState.curr_player+1), 1)
        printText("Dice one:", 2)
    lcd_clear()
    printText("player " + str(gameState.curr_player+1), 1)
    printText("Dice one:" + moves[0], 2)
    printText("Dice two:", 3)
    time.sleep(1)
    moves[1] = read_from_keyboard()
    while moves[1] < "1" or moves[1] > "6":
        moves[1] = read_from_keyboard()
        printText("Dice two:", 3)
        lcd_clear()
    printText("player " + str(gameState.curr_player+1), 1)
    printText("Dice one:" + moves[0], 2)
    printText("Dice two:" + moves[1], 3)
    time.sleep(1)
    lcd_clear()
    state = gameState.dice(moves)
    print_cell_info()
    process_turn(state)
    gameState.end_turn(moves)
