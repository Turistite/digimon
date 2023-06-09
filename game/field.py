from game.utils.enums import Status, FieldType


class Field:
    def __init__(self, prop_list):
        id, color, field_type, price, rents = prop_list
        # False means that its owned by the bank
        # "" would work too
        self.owner = False

        self.id = id
        self.color = color

        self.level = 0
        self.price = int(price)
        self.rents = [] if rents == 'null' else [
            int(r) for r in rents.split(',')]
        self.status = Status.FREE  # купено, ипотекирано, свободно
        self.building_type = FieldType[field_type.upper()]

    def get_rent(self, die_sum= 7):
        if not self.rents or self.status.name == Status.FREE.name:
            return self.price
        elif self.building_type == FieldType.SERVICES:
            return self.rents[self.level] * die_sum
        else:
            return self.rents[self.level]

    def upgrade(self):
        self.level += 1
        assert (self.level < len(self.rents))

    def mortgage(self):
        self.status = Status.MORTGAGED
        self.owner.balance += round(self.price * 0.5)
        self.owner.number_of_properties -= 1

    #  def buy(self, field, amount=False):
    def unmortgage(self):
        self.owner.buy(self, self.price * 1.1)

    def show(self):
        print(self.owner, self.level, self.price,
              self.rents, self.status, self.building_type)
