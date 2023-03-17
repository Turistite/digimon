class Field:
  def __init__(self, prop_list):
    owner, price, rent, status, upgradable = prop_list
    self.owner = owner# can be null/bank
    self.price = price
    self.rent = rent
    self.status = status# купено, ипотекирано, свободно
    self.upgradable = upgradable
