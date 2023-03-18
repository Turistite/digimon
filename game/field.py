from game.utils.enums import *

class Field:
    def __init__(self, prop_list):
        building_type, price, rents = prop_list
        self.owner = False  # default for owned by the bank
        self.level = 0
        self.price = price
        if rents == "null":
            self.rents = []
        else:
            self.rents = rents.split(',')
        self.status = 'free'  # купено, ипотекирано, свободно
        self.building_type = building_type

    def get_rent(self):
        # TODO: don't exceed the array length
        if len(self.rents) == 0:
            return int(self.price)
        return self.rents[self.level]

    def show(self):
        print(self.owner, self.level, self.price,
              self.rents, self.status, self.building_type)

    def upgrade():
        self.level += 1
        assert (self.level < len(self.rents))

    def mortgage():
        assert (self.status == Status.BOUGHT)
        self.status = Status.MORTGAGED

    def immortgage():
        assert (self.status == Status.MORTGAGED)
        self.status = Status.BOUGHT
