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
    print("await_end_of_turn")
    # TODO button


def read_nfc_card():
    print("read_nfc_card")


def display_on_screen(text):
    print("display_on_screen")


def auction():
    print("Enter auction function")
    value = gameState.fields[gameState.players[gameState.curr_player].position].price
    value = int(COEF_AUCTION*value)
    step = int(COEF_STEP*value)
    start = time.time()
    current_owner = -1

    while time.time() <= (start+5):
        printText(str(value), 1)
        id = try_to_read()
        if id != -1:
            lcd_clear()
            current_owner = get_player_by_id(id)
            start = time.time()
            time.sleep(1)
            value += step

    if current_owner != -1:
        # gameState.players[current_owner].buy(game
        printText("Successfully bought for " +value, 1)
        time.sleep(1.5)

    print("auction")


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
            auction()
        elif (id == gameState.players[gameState.curr_player].id):
            buy()
        else:
            print("Error")
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
    print("Before")
    time.sleep(0.8)
    lcd_clear()
    state = gameState.dice(moves)
    print("After")
    process_turn(state)
    gameState.end_turn()
