from game.utils.enums import Status, FieldType


class Field:
    def __init__(self, prop_list):
        color, field_type, price, rents = prop_list
        # False means that its owned by the bank
        # "" would work too
        self.owner = False

        self.id = '<id-goes-here>'
        self.color = color

        self.level = 0
        self.price = int(price)
        self.rents = [] if rents == 'null' else [int(r) for r in rents.split(',')]
        self.status = Status.FREE  # купено, ипотекирано, свободно
        self.building_type = FieldType[field_type.upper()]

    def get_rent(self, die_sum):
        if not self.rents:
            return self.price
        elif self.building_type == FieldType.SERVICES:
            return self.rents[self.level] * die_sum
        else:
            return self.rents[self.level]

    def upgrade(self):
        self.level += 1
        assert (self.level < len(self.rents))

    def show(self):
        print(self.owner, self.level, self.price,
              self.rents, self.status, self.building_type)
