from game.utils.enums import Status


class Player:
    # TODO: handle bankrupt
    def __init__(self, id, color, balance, position):
        self.id = id
        self.color = color
        self.balance = balance
        self.position = position
        self.captured = 0

    def move(self, n_tiles, board_size):
        self.position += n_tiles
        # Check if the player has passed the start field
        if self.position >= board_size:
            self.balance += 200

        self.position %= board_size

    def buy(self, field, amount=False):
        self.pay(field.price if not amount else amount)
        field.owner = self
        field.status = Status.BOUGHT

    def pay(self, amount, recipient=False):
        self.balance -= amount
        # If there is a recipient
        if recipient:
            recipient.balance += amount

    def show(self):
        print(self.id, self.color, self.balance, self.position)
