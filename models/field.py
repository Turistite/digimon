class Field:
  def __init__(self, prop_list):
    building_type, price, rents = prop_list
    self.owner = False # default for owned by the bank
    self.level = 0 # 1 if not property
    self.price = price
    self.rents = [int(x) for x in rents.split(',')]
    self.status = 'free' # купено, ипотекирано, свободно
    self.building_type = building_type

  def get_rent():
    # TODO: don't exceed the array length
    return self.rents[self.level]
