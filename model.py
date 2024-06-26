import random


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


class Player:
    bot_names = [
        'Feynman', 'Einstein', 'Dawkins', 'Curie', 'Newton', 'Gödel',
        'Mozart', 'Bach', 'Beethoven', 'Chopin', 'Zimmer', 'Tchaikovsky',
        'Van Gogh', 'Picasso', 'Rembrant', 'Monet', 'Dali', 'Munch',
    ]

    def __init__(self, name='', score=0):
        self.is_bot = self._is_bot(name)
        self.name = self._get_name(name)
        self.hand = Hand()
        self.score = score
        self.guess = 0
        self.round_wins = 0

    def _is_bot(self, name):
        return False if name else True

    def _get_name(self, name):
        if not name:
            randint = random.randint(0, len(self.bot_names)-1)
            name = self.bot_names[randint]
        return name

    def __str__(self):
        return self.name


class Round:
    """
    state = {
        "wins": {player: 0 for player in self.players},
        "dealt": {player: None for player in self.players},
        "dealer"; None,
        "player": None,
        "error": False,
        "message": "",
    }
    """
    def __init__(self, round, round_count, players):
        self.round = round
        self.round_count = round_count
        self.players = players
        self.first_player = None
        self.dealer = None
        self.wins = {player: 0 for player in self.players}
        self.deck = Deck()
        self.dealt = {player: None for player in self.players}
        self.start_index = 0
        self.last_win = None
        self.instructions = ''

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
        # print('\nThe wins so far in this round are:')
        # for player, score in self.wins.items():
        #     print(player, score)
        # print('\n')

    def _check_valid_play(self):
        pass

    def _validate_last_guess(self, guesser, max_guess):
        while True:
            sum_guesses = 0
            for player in self.players:
                sum_guesses += player.guess
            if not sum_guesses == max_guess:
                return
            try:
                guess = int(input(f'\t{guesser.__str__()}, invalid last guess. Try again: '))
                if not 0 <= guess <= max_guess:
                        continue
            except (TypeError, ValueError):
                continue
            guesser.guess = guess

    def _wrong_input(self, guesser, max_guess):
        while True:
            try:
                guess = int(input(f'\t{guesser.__str__()}, invalid input. Try again: '))
                if not 1 <= guess <= max_guess:
                     continue
            except (TypeError, ValueError):
                continue
            return guess

    def _get_first_player(self):
        if self.last_win:
            return self.players.index(self.last_win)
        guesses = [player.guess for player in self.players]
        return guesses.index(max(guesses))

    def _set_state(self):
        state = {
            
        }

    def play_round(self):
        for i in range(self.round):
            self.start_index = self._get_first_player()
            self.first_player = self.players[self.start_index]
            print(f'\n{self.first_player} starts playing\n')
            self.instructions = f'\n{self.first_player} starts playing\n'
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
        max_guess = self.round
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
                self._validate_last_guess(guesser, max_guess)
                print(f'\n{guesser} guessed {guesser.guess}. That was the last guess. Moving on')
                return
            print(f'\n{guesser} guessed {guesser.guess}. Next players turn.\n')

    def deal(self):
        num_cards = self.round
        for recipiant in self.players:
            print(f'Dealing {num_cards} to {recipiant.__str__()}')
            for i in range(num_cards):
                recipiant.hand.put(self.deck.deal())

    def init_round(self):
        print(f'\n\tRound {self.round_count + 1} is about to start.' \
              ' The standings are:')
        for player in self.players:
            print(f'\t\t{player.__str__()}: {player.score} points.')
        print(f'\n\t{self.players[-1].__str__()} is the dealer.')
        input('\tWhen ready, press Enter.\n')
        self.deck.shuffle()
        print('Deck shuffled - OK\n')

    def get_state(self, message, error):
        wins = {player.__str__(): wins for player, wins in self.wins.items()}
        dealt = {player.__str__(): dealt for player, dealt in self.dealt.items()}
        state = {
            "wins": wins,
            "dealt": dealt,
            "dealer": self.players[-1].__str__(),
            "player": self.first_player.__str__(),
            "error": error,
            "message": message,
        }
        return state


class Plump:
    """
    state = {
        "rounds": [2,3,2],
        "score": {player.__str__(): player.score for player in self.players},
        "round_count": 0,
        "game_over": False,
    }
    """
    round_options = {
        3: [2,3,2],
        5: [2,3,4,3,2],
        9: [2,3,4,5,6,7,5,4,3,2],
        15: [2,3,4,5,6,7,8,9,8,7,6,5,4,3,2],
    }

    def __init__(self, player_list, duration):
        self.players = []
        self.rounds = []
        self.round_count = 0
        self.game_over = False
        self._setup_game(player_list, duration)

    def _setup_game(self, player_list, duration):
        self.rounds = self.round_options[duration]
        for player in player_list:
            self.players.append(Player(player))

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

    def update_state(self, result):
        if self.round_count == len(self.rounds) - 1:
            self.game_over = True
            return
        self._give_points(result)
        self._arrange_wrt_dealer()
        self.round_count += 1

    def get_state(self):
        score = {player.__str__(): player.score for player in self.players}
        state = {
            "rounds": self.rounds,
            "score": score,
            "round_count": self.round_count,
            "game_over": self.game_over,
        }
        return state

    # def iterate(self):
    #     if self.game_over:
    #         return self.get_state()

    #     round_count = self.round_count
    #     round = Round(self.rounds[round_count], round_count, self.players)


    #     # result = round.play()
    #     round.init_round()
    #     round.deal()
    #     round.guess_wins()
    #     round.play_round()
    #     result = round.wins


    #     self.update_state(result)
    #     print(self.get_state())

    #     return self.get_state()