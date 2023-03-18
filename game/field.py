from game.utils.enums import Status, FieldType

class Field:
    def __init__(self, id, prop_list):
        field_type, price, rents = prop_list
        # False means that its owned by the bank
        # "" would work too
        self.owner = False

        self.level = 0
        self.price = price
        self.rents = [] if rents == 'null' else rents.split(',')
        self.status = Status.FREE  # купено, ипотекирано, свободно
        self.building_type = FieldType[field_type.upper()]

    def get_rent(self, die_sum):
        if len(self.rents) == 0:
            return int(self.price)
        elif self.building_type == FieldType.SERVICES:
            return self.rents[self.level] * die_sum
        else:
            return self.rents[self.level]

    def upgrade(self):
        self.level += 1
        assert (self.level < len(self.rents))

    def mortgage(self):
        assert (self.status == Status.BOUGHT)
        self.status = Status.MORTGAGED

    def immortgage(self):
        assert (self.status == Status.MORTGAGED)
        self.status = Status.BOUGHT

    def show(self):
        print(self.owner, self.level, self.price,
              self.rents, self.status, self.building_type)
