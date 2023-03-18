class Player:
  def __init__(self, id, color, balance, position):
    self.id = id
    self.color = color
    self.balance = balance
    self.position = position

  def move(dice_value):
    self.position += dice_value

  def buy(field):
    field.owner = self
    self.pay(field.get_rent())
  
  def pay(recipient,amount):
    recipient.balance+=amount
    self.balance-=amount

  def pay(amount):
    self.balance-=amount
  
  def show(self):
    print(self.id , self.color , self.balance , self.position)


def main():
    gs = Player(1,'red',1000,0)
    gs.show()


if __name__ == "__main__":
    main()