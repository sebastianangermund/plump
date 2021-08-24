import random
import time

from pygase import Client


class Card:
    ranks = ['Two', 'Three', 'Four', 'Five',
             'Six', 'Seven', 'Eight', 'Nine', 'Ten',
             'Jack', 'Queen', 'King' , 'Ace']
    suites = ['Diamonds', 'Clubs', 'Hearts']
    trump_suites = ['Spades']

    def __init__(self, rank=ranks[-1], suite=suites[-1]):
        self.suite = suite
        self.rank = rank
        self.cards = [f'{rank} of {suite}' for rank in self.ranks \
                        for suite in self.suites] \
                        + [f'{rank} of {suite}' for rank in self.ranks \
                        for suite in self.trump_suites]
        self.value_mapping = {card: index for index, card \
                                in enumerate(self.cards)}

    def __str__(self):
        return f'{self.rank} of {self.suite}'

    def __lt__(self, other):
        return self.value_mapping[self.__str__()] < self.value_mapping[other.__str__()]

    def __gt__(self, other):
        return self.value_mapping[self.__str__()] > self.value_mapping[other.__str__()]

    def __ge__(self, other):
        return (self.value_mapping[self.__str__()] > self.value_mapping[other.__str__()]) \
            or (self.value_mapping[self.__str__()] == self.value_mapping[other.__str__()])

    def __eq__(self, other):
        return self.value_mapping[self.__str__()] == self.value_mapping[other.__str__()]


class Deck:
    """ """
    def __init__(self):
        self.cards = [Card(rank, suite) for rank in Card.ranks \
                      for suite in Card.suites] \
                    + [Card(rank, suite) for rank in Card.ranks \
                      for suite in Card.trump_suites]

    def __str__(self):
        return f'{self.cards[0]}'

    def list_(self):
        return [card.__str__() for card in self.cards]

    def shuffle(self):
        random.shuffle(self.cards)

    def invert_(self):
        tmp = []
        for i in range(len(self.cards)):
            if not len(self.cards) > 1:
                break
            tmp2 = []
            compare = self.cards.pop()
            for i in range(len(self.cards)):
                if self.cards[-1] > compare:
                    tmp2.append(self.cards.pop())
            tmp.append(compare)
            tmp += tmp2
        self.cards = tmp + self.cards

    def deal(self, card=0):
        return self.cards.pop(card)

    def put(self, card):
        self.cards.append(card)


class Hand(Deck):
    def __init__(self):
        self.cards = []


class Player(Client):
    bot_names = [
        'Feynman', 'Einstein', 'Dawkins', 'Curie', 'Newton', 'Gödel',
        'Mozart', 'Bach', 'Beethoven', 'Chopin', 'Zimmer', 'Tchaikovsky',
        'Van Gogh', 'Picasso', 'Rembrant', 'Monet', 'Dali', 'Munch',
    ]

    def __init__(self, name=''):
        super().__init__()
        self.player_id = None
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)        
        self.name = name
        if not name:
            randint = random.randint(0, len(self.bot_names)-1)
            self.name = self.bot_names[randint]
        self.hand = Hand()
        self.score = 0
        self.guess = 0
        self.round_wins = 0

    def __str__(self):
        return self.name

    # "PLAYER_CREATED" event handler
    def on_player_created(self, player_id):
        # Remember the id the backend assigned the player.
        self.player_id = player_id

class Round:

    def __init__(self, dealer, round, rounds, players):
        self.dealer = dealer
        self.round_count = round
        self.rounds = rounds
        self.players = players
        self.wins = {player: 0 for player in self.players}
        self.deck = Deck()
        self.dealt = {player: None for player in self.players}
        self.start_index = 0
        self.last_win = None

    def _part_round_end(self):
        # update self.wins based on self.dealt
        suite = self.dealt[self.players[self.start_index]].suite
        highest = None, Card('Two', suite)
        for player, card in self.dealt.items():
            if card.suite == 'Spades':
                pass
            else:
                if card.suite != suite:
                    continue
            if card >= highest[1]:
                highest = player, card
        self.wins[highest[0]] += 1
        # reset the dealt pile
        self.dealt = {player: None for player in self.players}
        # set round winner for next round
        self.last_win = highest[0]
        # print standings
        print('\nThe wins so far in this round are:')
        for player, score in self.wins.items():
            print(player, score)
        print('\n')

    def _check_valid_play(self):
        pass

    def _wrong_input(self, guesser, max_guess, last_guess=False):
        if last_guess:
            while True:
                sum_guesses = 0
                for player in self.players:
                    sum_guesses += player.guess
                if not sum_guesses == max_guess:
                    return None
                try:
                    guess = int(input(f'\t{guesser.__str__()}, invalid last guess. Try again: '))
                    if not 0 <= guess <= max_guess:
                         continue
                except TypeError:
                    continue
                break
            return guess

        while True:
            try:
                guess = int(input(f'\t{guesser.__str__()}, invalid input. Try again: '))
                if not 0 <= guess <= max_guess:
                     continue
            except (TypeError, ValueError):
                continue
            return guess

    def _get_first_player(self):
        if self.last_win:
            return self.players.index(self.last_win)
        guesses = [player.guess for player in self.players]
        return guesses.index(max(guesses))

    def play_round(self):
        for i in range(self.round_count):
            self.start_index = self._get_first_player()
            print(f'\n{self.players[self.start_index]} starts playing\n')
            for j in range(len(self.players)):
                player = self.players[(self.start_index + j) % len(self.players)]
                print(f'\t{player}\'s hand: {player.hand.list_()}, with guess {player.guess}')
                try:
                    card = int(input(f'\t{player} play a card (1 - {len(player.hand.cards)}): '))
                    if not 1 <= card <= len(player.hand.cards):
                        card = self._wrong_input(player, len(player.hand.cards))
                except (TypeError, ValueError):
                    card = self._wrong_input(player, len(player.hand.cards))
                card -= 1
                self.dealt[player] = player.hand.deal(card)
                print('\nPile:')
                for player, card in self.dealt.items():
                    if self.players.index(player) == self.start_index:
                        print(f'{card} - LEAD CARD')
                    else:
                        print(card)
                print('\n')
            self._part_round_end()

    def guess_wins(self):
        max_guess = self.round_count
        for guesser in self.players:
            print(f'\n\t{guesser}\'s cards: {guesser.hand.list_()}')
            try:
                guess = int(input(f'\t{guesser.__str__()}, place your guess to how many rounds you\'ll win: '))
                if not 0 <= guess <= max_guess:
                     guess = self._wrong_input(guesser, max_guess)
            except (TypeError, ValueError):
                guess = self._wrong_input(guesser, max_guess)
            guesser.guess = guess
            if guesser is self.players[-1]:
                new_guess = self._wrong_input(guesser, max_guess, last_guess=True)
                if new_guess:
                    guesser.guess = new_guess
                print(f'\n{guesser} guessed {guesser.guess}. That was the last guess. Moving on')
                return
            print(f'\n{guesser} guessed {guesser.guess}. Next players turn.\n')

    def deal(self):
        num_cards = self.round_count
        for recipiant in self.players:
            print(f'Dealing {num_cards} to {recipiant.__str__()}')
            for i in range(num_cards):
                recipiant.hand.put(self.deck.deal())

    def init_round(self):
        print(f'\n\tRound {self.round_count - 1} is about to start.' \
              ' The standings are:')
        for player in self.players:
            print(f'\t\t{player.__str__()}: {player.score} points.')
        print(f'\n\t{self.dealer.__str__()} is the dealer.')
        input('\tWhen ready, press Enter.\n')
        self.deck.shuffle()
        print('Deck shuffled - OK\n')

    def play(self):
        self.init_round()
        self.deal()
        self.guess_wins()
        self.play_round()
        return self.wins

class Plump:
    """
    """
    durations = {
        5: [2,3,4,3,2],
        9: [2,3,4,5,6,7,5,4,3,2],
        15: [2,3,4,5,6,7,8,9,8,7,6,5,4,3,2],
    }

    def __init__(self, **kwargs):
        self.players = [Player(name) for name in kwargs['players']]
        self.rounds = self.durations[kwargs['duration']]
        self.ledger = self._set_game_ledger()
        self.round_count = 0

    def _set_game_ledger(self):
        ledger = {}
        for player in self.players:
            ledger[player] = [0 for el in range(len(self.rounds))]
        return ledger

    def _arrange_wrt_dealer(self):
        tmp = []
        for i in range(len(self.players)):
            tmp.append(self.players[(i + 1) % len(self.players)])
        self.players = tmp

    def _give_points(self, result):
        for player, wins in result.items():
            if player.guess == wins:
                if wins == 0:
                    player.score += 5
                else:
                    player.score += wins * 10

    def play(self):
        for round in self.rounds:
            dealer = self.players[-1]
            round = Round(dealer, round, self.rounds, self.players)
            result = round.play()
            self._give_points(result)
            self._arrange_wrt_dealer()
            self.round_count += 1
        print('\n'*10)
        print('End of game!\n\tFinal score was:')
        for player in self.players:
            print(player, player.score)

# Create a client.
client = Player()

### MAIN PROCESS ###

if __name__ == "__main__":
    # Connect the client, let the player input a name and join the server.
    client.connect_in_thread(hostname="localhost", port=8080)
    client.dispatch_event("JOIN", input("Player name: "))
    # Wait until "PLAYER_CREATED" has been handled.
    while client.player_id is None:
        pass
    # Start the actual main loop.
    game_loop_is_running = True
    while game_loop_is_running:
        # Safely access the synchronized shared game state.
        with client.access_game_state() as game_state:
            # Notify server about player movement.
            if old_game_message == game_state.message:
                time.sleep(1)
                continue
            if game_state.message:
                print(game_state.message, "\n")
            if not game_state.turn_id == client.player_id:
                continue
            client.dispatch_event(
                event_type="MOVE",
                player_id=client.player_id,
                new_position=int(input("new position")),
            )
            client.dispatch_event(
                event_type="MESSAGE",
                message = str(client.player_id) + " made a move",
            )
            # Print player scores.
            for player_id, player in game_state.players.items():
                if player_id == client.player_id:
                    # Yourself
                    print(f"Your position is {player['position']}")
                elif player_id == game_state.chaser_id:
                    # The chaser
                    print(f"The chaser is {player['name']} with position {player['position']}")
                else:
                    # Others
                    print(f"{player['name']} have position {player['position']}")

    # Disconnect afterwards and shut down the server if the client is the host.
    client.disconnect(shutdown_server=True)
