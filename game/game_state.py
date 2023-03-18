from game.utils.enums import Action, Status, PLAYER_COLORS, FieldType
from game.player import Player
from game.field import Field


class GameState:
    def __init__(self, ids):
        f = open('/home/pi/digimon/game/static/fields.txt', 'r')
        self.fields = [
            Field(1, line.rstrip('\n').split(';'))
            for line in f.readlines()
        ]

        ids_and_colors = zip(ids, PLAYER_COLORS[0:len(ids)])
        self.players = [
            Player(id, color, 1500, 0)
            for id, color in ids_and_colors
        ]

        self.curr_player = 0

    def get_player_by_id(self, id):
        players_with_id = filter(lambda p: p.id == id, self.players)
        if players_with_id:
            h, *_ = list(players_with_id)
            return h
        else:
            return False

    def dice(self, points):
        die1 = int(points[0])
        die2 = int(points[1])

        curr_player = self.players[self.curr_player]
        curr_field = self.fields[curr_player.position]

        if (curr_field.building_type.name == FieldType.PRISON.name
                and curr_player.captured > 0):
            if die1 == 6 and die2 == 6:
                self.captured = 0
            else:
                return Action.NOTHING

        curr_player.move(die1 + die2, len(self.fields))

        if (curr_field.owner == curr_player
                or curr_field.status.name == Status.MORTGAGED.name
                or curr_field.get_rent(points) == 0):
            return Action.NOTHING

        print(curr_field)
        if curr_field.status.name == Status.BOUGHT.name:
            # payment to owner   ???
            return Action.PAYMENT

        if curr_field.status.name == Status.FREE.name:
            return Action.PENDING
        # if curr_field.status == FieldType.ARREST
        # TODO cover case for Status.SPECIAL

    def upgrade_property(self, prop_ids):
        props_for_upgrade = filter(lambda f: f.id in prop_ids, self.fields)

        # TODO: check if the player meets the conditions to upgrade
        for p in props_for_upgrade:
            p.upgrade()
            self.players[self.curr_player].pay(0.6 * p.price)

    def end_turn(self):
        if self.curr_player.captured > 0:
            self.curr_player.captured -= 1

        self.curr_player = (self.curr_player + 1) % len(self.players)
