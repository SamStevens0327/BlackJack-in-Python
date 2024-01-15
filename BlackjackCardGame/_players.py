class Dealer:

    def __init__(self):
        self.hand = []
        self.hand_val = 0
        self.status = 0
        self.name = 'Dealer'

class Player(Dealer):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.wallet = 100000
        self.stash = 0
        self.bet = 0

