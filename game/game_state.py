from game.utils.enums import Action, Status, FieldType, PLAYER_COLORS
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

    def get_current_player(self):
        return self.players[self.curr_player]

    def __get_colored_fields(self, color):
        return filter(lambda f: f.color == color, self.fields)

    def __can_upgrade_property(self, player, field):
        neighbourhood = self.__get_colored_fields(field.color)
        levels = map(lambda n: n.level, neighbourhood)

        return (
            field.building_type.name == FieldType.PROPERTY.name
            and player.balance >= field.price * 0.6
            and all(map(lambda n: n.owner == player, neighbourhood))
            and max(levels) - min(levels) <= 1
        )

    def get_player_by_id(self, id):
        for p in self.players:
            if p.id == id:
                return p
        return False

    def get_field_by_id(self, id):
        for f in self.fields:
            if f.id == id:
                return f
        return False

    def dice(self, points):
        die1 = int(points[0])
        die2 = int(points[1])

        curr_player = self.get_current_player()
        curr_field = self.fields[curr_player.position]

        if (curr_field.building_type.name == FieldType.PRISON.name
                and curr_player.captured > 0):
            if die1 == 6 and die2 == 6:
                self.captured = 0
            else:
                return Action.NOTHING
        
        curr_player.move(die1 + die2, len(self.fields))
        curr_field = self.fields[curr_player.position]

        if (curr_field.building_type.name == FieldType.ARREST.name):
             curr_player.position = 10
             curr_player.captured = 3
             if(curr_player.balance < 50):
                get_field_by_id(2).mortgage()
                # TODO some things with NFC
             curr_player.balance -= 50
             return Action.NOTHING
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

    def upgrade_property(self, property):
        # TODO: Use this in the future:
        #  property = self.get_field_by_id(id)
        curr_player = self.get_current_player()
        if self.__can_upgrade_property(curr_player, property):
            property.upgrade()
            curr_player.pay(0.6 * property.price)
            return True
        else:
            return False

    def end_turn(self, moves):
        if self.players[self.curr_player].captured > 0:
            self.players[self.curr_player].captured -= 1
        if moves[0] != moves[1]:
           self.curr_player = (self.curr_player + 1) % len(self.players)
