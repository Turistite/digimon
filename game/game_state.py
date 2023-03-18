from game.field import *
from game.player import *
from game.utils.enums import *

class GameState:
    def __init__(self, ids):
        f = open('static/fields.txt', 'r')
        self.fields = [
            Field(line.rstrip('\n').split(';'))
            for line in f.readlines()
        ]

        ids_and_colors = zip(ids, PLAYER_COLORS[1:len(ids)])
        self.players = [
            Player(id, color, 1500, 0)
            for id, color in ids_and_colors
        ]

        self.curr_player = 0

    def dice(self, points):
        curr_player = self.players[self.curr_player]
        curr_field = self.fields[curr_player.position]

        curr_player.position += points

        curr_player.move(points, len(self.fields))

        if curr_field.owner == curr_player or curr_field.status == Status.MORTGAGED or curr_field.get_rent() == 0:
            return Action.NOTHING

        if curr_field.status == Status.BOUGHT:
            # payment to owner   ???
            return Action.PAYMENT

        if curr_field.status == Status.FREE:
            return Action.OTHER
            # to be determined  ???
            # buying or auctioning or nothing

        # TODO cover case for Status.SPECIAL

    def end_turn(self):
        self.curr_player = (self.curr_player+1) % len(self.players)


def main():
    gs = GameState(['Nakata', 'Kalata', 'bot1', 'bot2'])
    for x in gs.fields:
        x.show()
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)
    gs.dice(6)
    print(gs.players[gs.curr_player].balance)


if __name__ == "__main__":
    main()
