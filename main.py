from game.game_state import GameState
from game.utils.enums import Action
from hardware.CardRead import *
from hardware.keyboard import *
import time

nfc_id_auction = 633367768675

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5


def await_end_of_turn():
    printText("\# to see balance",1)
    printText("* to upgrade",2)
    printText("A/B to mortgage",3)
    printText("any other to end the turn",4)
    key =  read_from_keyboard()
    # ti si tuka !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # wzima 1 character ot keyboard
    # ako precenish gi  mesti w keyboard.py inche tuka
    if key=='#':
        lcd_clean() # proveri towa li izchistwashe dyskata !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pintText("Your balance is: " + str(gameState.players[gameState.curr_player].balance),2)
        time.sleep(3)
        lcd_clean()
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
    print("Enter auction function")
    value = gameState.fields[gameState.players[gameState.curr_player].position].price
    value = int(COEF_AUCTION*value)
    field = gameState.fields[gameState.players[gameState.curr_player].position]
    step = int(COEF_STEP*value)
    current_owner = False

    wait=0
    while wait<5:
        wait+=1
        printText(str(value), 1)
        id = try_to_read()
        if id:
            lcd_clear()
            print(id)
            current_owner = gameState.get_player_by_id(id)
            start = time.time()
            time.sleep(1)
            value += step
            wait=0
        time.sleep(1)

    if current_owner:
        current_owner.buy(field,value)
        printText("Successfully bought for " +str(value), 1)
        time.sleep(1.5)

    await_end_of_turn()


def buy():
    print("Enter buy function")
    gameState.players[gameState.curr_player].buy(
        gameState.fields[gameState.players[gameState.curr_player].position]
    )


def process_turn(status):
    if status == Action.NOTHING:
        await_end_of_turn()
    elif status == Action.PAYMENT:
        buy()
        await_end_of_turn()
    elif status == Action.PENDING:
        print("pending action")
        id = wait_for_a_card()
        if id == nfc_id_auction:
            time.sleep(1)
            auction()
        elif (id == gameState.players[gameState.curr_player].id):
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
    time.sleep(0.2)
    lcd_clear()
    list_id = []
    for i in range(players_count):
        printText("Scan player " + str(i+1) + " card", 2)
        time.sleep(0.5)
        curr_id = wait_for_a_card()
        list_id.append(curr_id)
        print(list_id)
        lcd_clear()
    return list_id


def proccess_action():
    # TODO stuff
    # proccessing functions
    print("Something")


players_ID = players_id()
gameState = GameState(players_ID)

while True:
    printText("Enter what dices have been thrown!", 1)
    time.sleep(1)
    lcd_clear()
    printText("Dice one:", 1)
    moves = [0, 0]
    moves[0] = read_from_keyboard()
    while moves[0] < "1" or moves[0] > "6":
        moves[0] = read_from_keyboard()
        lcd_clear()
        printText("Dice one:", 1)
    lcd_clear()
    printText("Dice one:" + moves[0], 1)
    printText("Dice two:", 2)
    time.sleep(1)
    moves[1] = read_from_keyboard()
    while moves[1] < "1" or moves[1] > "6":
        moves[1] = read_from_keyboard()
        printText("Dice two:", 2)
        lcd_clear()
    printText("Dice one:" + moves[0], 1)
    printText("Dice two:" + moves[1], 2)
    time.sleep(0.8)
    lcd_clear()
    state = gameState.dice(moves)
    process_turn(state)
    gameState.end_turn(moves)
