class ChanceCard:
    # The idea is to hard code a list of constructed chance cards in the game state
    # a lambda function is passed, that represents self.effect
    #
    # When a player steps on a chance card,
    # he would scan it and effect() should then be called
    def __init__(self, effect, prop_list):
        id = prop_list
        self.id = id
        self.effect = effect
