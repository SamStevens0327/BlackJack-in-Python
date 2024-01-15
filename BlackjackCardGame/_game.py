import random
import sys
from _players import Player
from _players import Dealer
from _deck import cards
from _deck import royals

def start_game():
    while True:
        request = input("Type 'yes' to start or 'no' to exit; then hit Enter: ").lower()

        if request == "yes":
            print('\n'
                  '---------------------\n'
                  "Welcome to BlackJack!\n"
                  '---------------------\n\n')
            start = True
            break
        elif request == "no":
            start = False
            break
        else:
            print("Enter either 'yes' or 'no'...")

    return start
    print("Exiting the program.")
    sys.exit()


def invite_players(players):
    print(
        "Enter the names of all the players. "
        "Once all players are entered, type done to save the names.\n"
        )
    count = 1
    while True:
        player_name = input(f"Enter name of player {count}: ")

        if len(player_name) > 12:
            print("Name can be max 12 characters long")
        elif player_name.isspace() == True:
            print("Enter a name...")
        elif len(player_name) < 1:
            print("Please enter at least a character as a name.")
        elif player_name.lower() == "done":
            break
        else:
            new_player = Player(player_name)
            players.append(new_player)
            count += 1

    return players


def buy_sell_chips(players):
    for i in range(len(players)):
        players[i].status = 0
        while True:                                         # player buys chips
            x = input(f"\n{players[i].name}: How much chips would you like to buy?\n"
                      'Use a negative number to sell.'
                      '"Cash in" so sell all your chips.')
            if x.lower() == 'cash in':
                players[i].wallet += players[i].stash
                players[i].stash = 0
            try:
                x = float(x)
            except ValueError:
                print("Use a number!\n")
                continue
            if x == 0:                                      # no buy
                print(f"You have ${players[i].stash} of chips to play with.\n")
                break
            elif x > 100000:                                # too much
                print("Max buy is $100,000\n")
            elif x > 100 and x < 100000:                    # acceptable buy
                players[i].stash += x
                players[i].wallet -= x
                print(f"You have ${players[i].stash} available to play with.\n")
                break
            elif x > 0 and x < 100:                         # too little
                print("Minimum buy is $100.\n")
            elif x < 0 and abs(x) < players[i].stash:       # selling
                players[i].stash -= abs(x)
                players[i].wallet += abs(x)
                print(f"You now have ${players[i].stash} of chips to play with.\n")
                break
            elif x < 0 and abs(x) > players[i].stash:        
                print("You don't have that many chips to sell.\n")

    return players


def new_decks():
    while True:
        num_decks = input('How many decks will we be playing with?.')
        try:
            num_decks = int(num_decks)
        except ValueError:
            print('Enter a number.')
            
        deck = {key: [value[0], num_decks] for key, value in cards.items()}
        break
        
    return deck


def buy_in(x, players):
    print(f"The minimum buy in for this round is ${x}\n")       

    remaining_players = []
    broke_players = []                                  # filter out broke players
    for i in range(len(players)):
        if players[i].stash < x:
            print(f"{players[i].name} could not afford the buy in.")
            broke_players.append(players[i])
        elif players[i] not in broke_players:
            players[i].stash -= x
            players[i].bet += x
            remaining_players.append(players[i])

    return remaining_players


def deal(table):

    print("Dealing...")

    for _ in range(2):                                    # deals twice                
        for i in range(len(table[0])):                       # deals a card to each player
            card = random.choice(list(table[1].keys()))
            table[0][i].hand.append(card)
            table[0][i].hand_val += table[1][card][0]
            if table[1][card][1] > 1:
                table[1][card][1] -= 1
            else:
                table[1].pop(card)

    
    return [table[0], table[1]]


def bet(table):
    
    print("Betting round:\n")

    for i in range(len(table[0])):
        if table[0][i].status != 2:
            print(f"{table[0][i].name}, your hand is {table[0][i].hand}")
            while True:
                bet = input("What is your bet? ")                           # player bets
                if bet.lower() == "fold":                                   # fold
                    print(f"{table[0][i].name} folded.")
                    table[0][i].hand_val = 0
                    table[0][i].status = 2
                    break
                elif bet.lower() == 'all in' or 'max' or 'all':             # all in
                    table[0][i].bet += table[0][i].stash
                    table[0][i].stash = 0
                    break
                elif bet.lower() == 'check':
                    break
                else:
                    try:
                        bet = float(bet)                                    # bet value
                    except ValueError:
                        print("Use a number!")
                        continue
                    if bet < 0:
                        print("Positive number please!")
                        continue
                    elif bet >= 0 and bet < table[0][i].stash:
                        table[0][i].stash -= bet
                        table[0][i].bet += bet
                        table[0][i].status = 0
                        break
                    elif bet > table[0][i].stash:
                        print("You don't have that many chips to bet.")
                        continue
        else:
            print(f"{table[0][i].name} is not in this round.")
            continue

    return [table[0], table[1]]


def play(table):

    for i in range(len(table[0])):       # loop through players
        if table[0][i].status == 0: 
            print("Dealing round...")      
            while True:
                play = input(f"{table[0][i].name}:\n"
                            f"Your hand is: {table[0][i].hand}\n\n"
                            "Would you like to hit or stick?")      # players plays
                
                if play.lower() == 'hit':                           # hit
                    card = random.choice(list(table[1].keys()))
                    table[0][i].hand.append(card)
                    table[0][i].hand_val += table[1][card][0]
                    if table[0][i].hand_val > 21:
                        print('BUST!\n')
                        table[0][i].hand = ['BUST!']
                        table[0][i].hand_val = 0
                        table[0][i].status = 2
                    if table[1][card][1] > 1:
                        table[1][card][1] -= 1
                    else:
                        table[1].pop(card)
                    break
                elif play.lower() == 'stick':                       # stick
                    table[0][i].status = 1
                    break
                elif play.lower() == 'fold':                        # fold
                    table[0][i].hand_val = 0
                    table[0][i].status = 2
                    print(f"{table[0][i].name} folded.")
                    break
                else:
                    print("Say either 'Hit' or 'Stick'!")
        else:
            continue

    return [table[0], table[1]]


def dealer(table):
    people = []
    for i in range(len(table[0])):
        people.append(table[0][i])
    dealer = Dealer()
    for _ in range(2):
        card = random.choice(list(table[1].keys()))
        dealer.hand.append(card)
        dealer.hand_val += table[1][card][0]
        table[1].pop(card)
    while dealer.status == 0:
        print(f"Dealer's hand is {dealer.hand}\n")
        play = input('Hit or Stick?\n')
        if play.lower() == 'hit':
            card = random.choice(list(table[1].keys()))
            dealer.hand.append(card)
            dealer.hand_val += table[1][card][0]
            table[1].pop(card)
            if dealer.hand_val > 21:
                dealer.hand_val = 0
                dealer.hand = ['BUST!']
                dealer.status = 2
                print('BUST!')
        elif play.lower() == 'stick':
            dealer.status = 1
        else:
            print('Hit or Stick?\n')

    people.append(dealer)

    return people


def get_winner(players: list[Player]):
    pot = 0
    for i in range(len(players)):
        if players[i].name != 'Dealer':
            pot += players[i].bet
            players[i].bet = 0

    new_winner = Player('Winner')

    for i in range(len(players)):
        if players[i].hand_val > new_winner.hand_val:           # new winner
            new_winner = players[i]
        elif players[i].hand_val == new_winner.hand_val:        # find highest face value
            for a in players[i].hand:
                for b in new_winner.hand:
                    for card in royals.reverse():
                        if card == players[i].hand[a] and card == new_winner.hand[b]:
                            continue
                        elif card == players[i].hand[a] and card != new_winner.hand[b]:
                            new_winner = players[i]
                            break
                        elif card != players[i].hand[a] and card == new_winner.hand[b]:
                            break
                        else:
                            continue
        else:
            continue
    if new_winner.name != 'Dealer':
        new_winner.stash += pot

    return new_winner


def round_reset(table):
    for i in range(len(table[0])):
        table[0][i].hand.clear()
    
    while True:                                                             # decision to restart
        request = input('Would you like tp play another round?\n'
            "Type 'yes' to play or 'no' to Quit; then hit Enter: ").lower()

        if request == "yes":
            request = True
            print('\n'
                '--------------------\n'
                "The game must go on!\n"
                '--------------------\n\n')
            break
        elif request == "no":
            request = False
            break
        else:
            print("Enter either 'yes' or 'no'...")

    if request == True:
        
        table[1] = new_decks()
        
        while True:
            invite_request = input("Should we add more players to the game?")
            if invite_request.lower() == 'yes':
                table[0] = invite_players(table[0])
                break
            elif invite_request.lower() == 'no':
                break
            else:
                print('Enter "yes" or "no".')
                continue
        
        while True:
            if invite_request.lower() == 'yes':
                table[0] = buy_sell_chips(table[0])
                break
            else:
                exchange = input('Would you like to buy/sell chips.')
                if exchange.lower() == 'no':
                    break
                elif exchange.lower() == 'yes':
                    table[0] = buy_sell_chips(table[0])
                    break
                else:
                    print('Enter "yes" or "no".')
                    continue

    return request
    