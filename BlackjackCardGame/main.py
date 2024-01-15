import _game

request = _game.start_game()
if request == False:
    quit
else:
    players = _game.invite_players([])     # players sit at table

    deck = _game.new_decks()

    players = _game.buy_sell_chips(players)      # players buy/sell chips

    state = True
    while state == True:
        buy_in = 50
        players = _game.buy_in(buy_in, players)      # players put money on the table

        table = _game.deal([players, deck])      # outputs current [players, deck]

        status = []
        while status == [] or 0 in status:               # checks if players still in game 
            status.clear()

            bet = _game.bet(table)        # players bet on hand

            table = _game.play(bet)       # hit or stick

            for i in range(len(table[0])):
                status.append(table[0][i].status)
            
        people = _game.dealer(table)     # dealer plays cards

        winner = _game.get_winner(people)

        print(f"The winner is {winner.name}, with the hand: {winner.hand}\n\n")

        state = _game.round_reset(table)
    
quit

    