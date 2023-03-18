from field import *
from player import *
from colors import *
from actions import *


class GameState:
    def __init__(self, ids):
        f = open(
            'C:\\Users\\KaloyanTs\\Documents\\GitHub\\FMI_Codes\\digimon\\static\\fields.txt', 'r')
        self.fields = [Field(l.rstrip('\n').split(';')) for l in f.readlines()]

        ids_and_colors = zip(ids, all_colors[1:len(ids)])
        # NOTE: The initial balance is usually 15mil
        self.players = list(map(lambda pair: Player(
            pair[0], pair[1], 15000, 0), ids_and_colors))
        self.curr_player = 0

    def dice(points):
        self.players[self.curr_player].pos = (
            self.players[self.curr_player].position + points) % len(self.fields)
        if self.fields[self.players[self.curr_player].pos].owner == self.players[self.curr_player] or self.fields[self.players[self.curr_player].pos].status == 'mortgaged' or self.fields[self.players[self.curr_player].pos].get_rent() == 0:
            return Action.NOTHING
        if self.fields[self.players[self.curr_player].pos].status == Status.BOUGHT:
            # payment to owner   ???
            return Action.PAYMENT
        if self.fields[self.players[self.curr_player].pos].status == Status.FREE:
            return Action.OTHER
            # to be determined  ???
            # buying or auctioning or nothing

    def end_turn(self):
        self.curr_player = (self.curr_player+1) % len(self.players)


def main():
    gs = GameState(['Nakata', 'Kalata', 'bot1', 'bot2'])


if __name__ == "__main__":
    main()
