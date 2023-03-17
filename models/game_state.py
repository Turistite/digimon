from field import *

class GameState:
  def __init__(self):
    f = open('../static/fields.txt', 'r')
    self.fields = [Field(l.rstrip('\n').split(',')) for l in f.readlines()]

print([f.rent for f in GameState().fields])
