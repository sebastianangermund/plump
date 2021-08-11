import random


class Card:
    ranks = ['Two', 'Three', 'Four', 'Five',
             'Six', 'Seven', 'Eight', 'Nine', 'Ten',
             'Jack', 'Queen', 'King', 'Ace']
    suites = ['Diamonds', 'Clubs', 'Hearts', 'Spades']

    def __init__(self, rank=ranks[-1], suite=suites[-1]):
        self.suite = suite
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suite}'

    def __lt__(self, other):
        return Deck.value_mapping[self.__str__()] < Deck.value_mapping[other.__str__()]

    def __gt__(self, other):
        return Deck.value_mapping[self.__str__()] > Deck.value_mapping[other.__str__()]

    def __eq__(self, other):
        return Deck.value_mapping[self.__str__()] == Deck.value_mapping[other.__str__()]


class Deck:
    cards = [f'{rank} of {suite}' for rank in Card.ranks for suite in Card.suites]
    value_mapping = {card: index for index, card in enumerate(cards)}

    def __init__(self):
        self.cards = [Card(rank, suite) for rank in Card.ranks \
                      for suite in Card.suites]

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


class Player:
    bot_names = [
        'Feynman', 'Einstein', 'Dawkins', 'Curie', 'Newton', 'Gödel',
        'Mozart', 'Bach', 'Beethoven', 'Chopin', 'Zimmer', 'Tchaikovsky',
        'Van Gogh', 'Picasso', 'Rembrant', 'Monet', 'Dali', 'Munch',
    ]

    def __init__(self, name='', score=0):
        self.name = name
        if not name:
            randint = random.randint(0, len(self.bot_names)-1)
            self.name = self.bot_names[randint]
        self.hand = Hand()
        self.score = score
        self.guess = 0
        self.round_wins = 0

    def __str__(self):
        return self.name


class Round:

    def __init__(self, dealer, round_count, rounds, players):
        self.dealer = dealer
        self.round_count = round_count
        self.rounds = rounds
        self.players = players
        self.deck = Deck()
        self.dealt = {}

    def _part_round_end(self):
        results = self.dealt
        # give "rund winner points"
        # arrange player list
        # put back cards in deck

    def _round_end(self):
        pass
        # give winners points based on guess
        # reset dealt dict

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

    def _check_valid_play(self):
        pass

    def _get_first_player(self):
        guesses = [player.guess for player in self.players]
        return guesses.index(max(guesses))

    def play_round(self, start_index):
        for i in range(len(self.players)):
            player = self.players[(start_index + i) % len(self.players)]
            print(f'\t{player}\'s hand: {player.hand.list_()}')
            try:
                card = int(input(f'\t{player} play a card (1 - {len(player.hand.cards)}): '))
                if not 1 <= card <= len(player.hand.cards):
                     card = self._wrong_input(player, len(player.hand.cards))
            except (TypeError, ValueError):
                card = self._wrong_input(player, len(player.hand.cards))
            card -= 1
            self.dealt[player] = {'card': player.hand.deal(card)}
            print('\nPile:')
            for player, dict in self.dealt.items():
                print(dict['card'])
            print('\n')

    def guess_wins(self):
        max_guess = self.rounds[self.round_count]
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
        num_cards = self.rounds[self.round_count]
        for recipiant in self.players:
            print(f'Dealing {num_cards} to {recipiant.__str__()}')
            for i in range(num_cards):
                recipiant.hand.put(self.deck.deal())

    def init_round(self):
        print(f'\n\tRound {self.round_count + 1} of {len(self.rounds)} is about to start.' \
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
        start_index = self._get_first_player()
        print(f'\n{self.players[start_index]} starts playing\n')
        self.play_round(start_index)
        for player in self.players:
            print(player, player.hand.list_(), player.guess)


class Plump:
    """
    """
    durations = {
        5: [2,3,4,3,2],
        9: [2,3,4,5,6,7,5,4,3,2],
        15: [2,3,4,5,6,7,8,9,8,7,6,5,4,3,2],
    }

    def __init__(self, **kwargs):
        humans = [Player(name) for name in kwargs['players']]
        bots = [Player() for i in range(kwargs['num_bots'])]
        self.players = humans + bots
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
        self.dealer = self.players[0]

    def _update_ledger(self, result):
        pass

    def play(self):
        for round in self.rounds:
            dealer = self.players[0]
            round = Round(dealer, self.round_count, self.rounds, self.players)
            result = round.play()
            self._update_ledger(result)
            self._arrange_wrt_dealer()
            self.round_count += 1
