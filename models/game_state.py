from field import *
from utils.enums import *

class GameState:
    def __init__(self, ids):
        f = open('../static/fields.txt', 'r')
        self.fields = [Field(l.rstrip('\n').split(';')) for l in f.readlines()]

        ids_and_colors = zip(ids, all_colors[1:len(ids)])
        # NOTE: The initial balance is usually 15mil
        self.players = list(map(lambda pair: Player(
            pair[0], pair[1], 15000, 0), ids_and_colors))
        self.curr_player = 0

    def dice(self, points):
        self.players[self.curr_player].position += points
        if self.players[self.curr_player].position >= len(self.fields):
            # passed the 'start' field
            self.players[self.curr_player].balance += self.fields[0].get_rent()
        self.players[self.curr_player].position %= len(self.fields)
        if self.fields[self.players[self.curr_player].position].owner == self.players[self.curr_player] or self.fields[self.players[self.curr_player].position].status == Status.MORTGAGED or self.fields[self.players[self.curr_player].position].get_rent() == 0:
            return Action.NOTHING
        if self.fields[self.players[self.curr_player].position].status == Status.BOUGHT:
            # payment to owner   ???
            return Action.PAYMENT
        if self.fields[self.players[self.curr_player].position].status == Status.FREE:
            return Action.OTHER
            # to be determined  ???
            # buying or auctioning or nothing

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
