from game.utils.enums import Action, Status, PLAYER_COLORS, FieldType
from game.player import Player
from game.field import Field


class GameState:
    def __init__(self, ids):
        f = open('/home/pi/digimon/game/static/fields.txt', 'r')
        self.fields = [
            Field(line.rstrip('\n').split(';'))
            for line in f.readlines()
        ]

        ids_and_colors = zip(ids, PLAYER_COLORS[0:len(ids)])
        self.players = [
            Player(id, color, 1500, 0)
            for id, color in ids_and_colors
        ]

        self.curr_player = 0

    def dice(self, points):
        curr_player = self.players[self.curr_player]
        curr_field = self.fields[curr_player.position]

        if (curr_field.building_type == FieldType.PRISON
                and curr_player.captured > 0
                and not self.jail(points)):
            return Action.NOTHING

        curr_player.move(points, len(self.fields))

        if (curr_field.owner == curr_player
                or curr_field.status == Status.MORTGAGED
                or curr_field.get_rent() == 0):
            return Action.NOTHING

        if curr_field.status == Status.BOUGHT:
            # payment to owner   ???
            return Action.PAYMENT

        if curr_field.status == Status.FREE:
            return Action.PENDING
        # if curr_field.status == FieldType.ARREST
        # TODO cover case for Status.SPECIAL

    def jail(self, dice):
        if(dice[0] == dice[1]):
            self.curr_player.captured = 0
            return True
        elif (False):  # TODO
            return True
           # TODO prompt if the player wants to pay to be free
        else:
            self.curr_player.captured -= 1
            return False

    def upgrade_property(self, prop_ids):
        props_for_upgrade = filter(lambda f: f.id in prop_ids, self.fields)

        # TODO: check if the player owns the whole neighbourhood
        for p in props_for_upgrade:
            p.upgrade()
            self.players[self.curr_player].pay(0.6 * p.price)

    def end_turn(self):
        self.curr_player = (self.curr_player + 1) % len(self.players)
