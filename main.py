from game.game_state import GameState
from game.utils.enums import Action
from hardware.CardRead import *
from hardware.keyboard import *
from game.field import *
import time

nfc_id_auction = 633367768675

COEF_AUCTION = 0.7
COEF_STEP = 0.05
TIMEOUT = 5


def print_cell_info():
    print(gameState.fields[gameState.players[gameState.curr_player].position])


def print_info():
    for player in gameState.players:
        print(str(player.color) + str(player.balance))


def await_end_of_turn():
    print_info()
    lcd_clear()
    printText("0 to see balance", 1)
    printText("* to upgrade", 2)
    printText("A/B to mortgage", 3)
    printText("any other to end", 4)
    key = read_from_keyboard()
    if key == '0':
        lcd_clear()
        printText("Your balance is: ", 2)
        printText(str(gameState.players[gameState.curr_player].balance), 3)
        time.sleep(3)
        lcd_clear()
        await_end_of_turn()
    elif key == "*":
        print("Upgrade property!")
        lcd_clear()
        printText("Upgrade propery!", 1)
        printText("Scan a property card", 2)
        id = wait_for_a_card()
        print(gameState.get_field_by_id(id))
        while (id!=nfc_id_auction) and ((gameState.get_field_by_id(id) == False) or gameState.get_field_by_id(id).owner != gameState.get_current_player()):
            printText("Invalid card!", 3)
            id = wait_for_a_card()
        lcd_clear()
        if id!=nfc_id_auction:
            curr_field = gameState.get_field_by_id(id)
            printText("Scan a card to pay", 1)
            printText(str(curr_field.price * 0.5) + " for a house", 2)

            id_player = wait_for_a_card()
            while id_player != gameState.players[gameState.curr_player].id:
                printText("Invalid card!", 3)
                id_player = wait_for_a_card()

            gameState.upgrade_property(gameState.get_field_by_id(id))

            lcd_clear()
            printText("Successfully built", 2)
            time.sleep(2)
            lcd_clear()

        await_end_of_turn()
    elif key == "A":
        lcd_clear()
        if gameState.get_current_player().number_of_properties > 0:
            printText("Scan the field to be mortgaged", 2)
            id = wait_for_a_card()
            gameState.get_field_by_id(id).mortgage()
        else:
            printText("No properties to sale", 2)
        await_end_of_turn()
    elif key == "B":
        lcd_clear()
        printText("Scan the field that you want unmortgaged", 2)
        id = wait_for_a_card()
        gameState.get_field_by_id(id).unmortgage()
        await_end_of_turn()
    else:
        return

def auction():

    lcd_clear()
    print("Enter auction function")
    printText("--Auction--", 1)
    value = gameState.fields[gameState.players[gameState.curr_player].position].price
    value = int(COEF_AUCTION*value)
    field = gameState.fields[gameState.players[gameState.curr_player].position]
    step = int(COEF_STEP*value)
    current_owner = False

    wait = 0
    while wait < 5:
        wait += 1
        printText("Current price:", 2)
        printText(str(value), 3)
        id = try_to_read()
        if id:
            lcd_clear()
            print(id)
            current_owner = gameState.get_player_by_id(id)
            start = time.time()
            # time.sleep(1)
            value += step
            wait = 0
        time.sleep(1)

    if current_owner:
        current_owner.buy(field, value)
        lcd_clear()
        printText("Successfully bought for " + str(value), 1)
        time.sleep(1.5)
        lcd_clear()

    await_end_of_turn()


def buy():
    print("Enter buy function")
    gameState.players[gameState.curr_player].buy(
        gameState.fields[gameState.players[gameState.curr_player].position]
    )


def handle_pay(player, field):
    price = field.get_rent()

    if player.balance < price:
        if player.number_of_properties > 0:
            printText("No money", 1)
            printText("Mortgage property:", 2)
            id = wait_for_a_card()
            mortgage(gameState.get_field_by_id(id))
        else:
            gameState.eliminate_player(player)
            gameState.end_turn((1, 2))
            return

    player.pay(field.get_rent(), field.owner)


def process_turn(status):
    curr_player = gameState.get_current_player()
    curr_field = gameState.fields[curr_player.position]

    if status == Action.NOTHING:
        await_end_of_turn()
    elif status == Action.PAYMENT:
        printText("Pay rent: " + str(curr_field.get_rent()), 2)
        id = wait_for_a_card()
        while id != gameState.players[gameState.curr_player].id:
            printText("Invalid card!", 3)
            id = wait_for_a_card()
        handle_pay(curr_player, curr_field)
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
            printText("Card not valid", 2)
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


players_ID = players_id()
gameState = GameState(players_ID)

while True:
    lcd_clear()
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
