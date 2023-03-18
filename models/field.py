class Field:
    def __init__(self, prop_list):
        building_type, rents, price = prop_list
        self.owner = False  # default for owned by the bank
        self.level = 0 if building_type == 'property' else 1
        self.price = price
        if rents == "null":
            self.rents = []
        else:
            self.rents = rents.split(',')
        self.status = 'free'  # купено, ипотекирано, свободно
        self.building_type = building_type

    def get_rent():
        # TODO: don't exceed the array length
        return self.rents[self.level]

    def show(self):
        print(self.owner, self.level, self.price,
              self.rents, self.status, self.building_type)

    def upgrade():
        self.level += 1
        assert (self.level < len(self.rents))

    def mortgage():
      assert(self.status=='bought')
        self.status = 'mortgaged'

    def immortgage():
        assert(self.status=='mortgaged')
        self.status = 'bought'
