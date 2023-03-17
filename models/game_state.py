from field import *
from player import *

class GameState:
  # TODO: add current player?
  def __init__(self, ids):
    f = open('../static/fields.txt', 'r')
    self.fields = [Field(l.rstrip('\n').split(';')) for l in f.readlines()]

    ids_and_colors = zip(ids, ['red', 'blue', 'green', 'yellow'])
    # NOTE: The initial balance is usually 15mil
    self.players = map(lambda id,col: Player(id, col, 15000, 0), ids_and_colors)
