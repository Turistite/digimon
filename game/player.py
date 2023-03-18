class Player:
    def __init__(self, id, color, balance, position):
        self.id = id
        self.color = color
        self.balance = balance
        self.position = position

    def move(self, n_tiles, board_size):
        self.position += n_tiles
        # Check if the player has passed the start field
        if self.position >= board_size:
            self.balance += 200

        self.position %= board_size

    def buy(self, field, amount=False):
        self.pay(False, field.price if not amount else amount)
        field.owner = self

    def pay(self, recipient, amount):
        self.balance -= amount
        # If there is a recipient
        if recipient:
            recipient.balance += amount

    def show(self):
        print(self.id, self.color, self.balance, self.position)
