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

    def invert(self):
        tmp = []
        for _ in range(len(self.cards)):
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

    def _get_min_card(self, cards):
        if not cards:
            return []
        min = cards[0]
        for card in cards:
            if card < min:
                min = card
        return min

    def sort(self):
        sorted = []
        new_cards = self.cards
        for _ in range(len(self.cards)):
            sorted.append(self._get_min_card(new_cards))
            new_cards = [card for card in self.cards if card not in sorted]
        self.cards = sorted

    def deal(self, card=0):
        return self.cards.pop(card)

    def put(self, card):
        self.cards.append(card)


class Hand(Deck):
    def __init__(self):
        self.cards = []

    def got_spades(self):
        suites = set([card.suite for card in self.cards])
        return set(Card.trump_suites).intersection(suites)


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
        self.guess = None
        self.round_wins = 0

    def __str__(self):
        return self.name

    def _is_bot(self, name):
        return False if name else True

    def _get_name(self, name):
        if not name:
            randint = random.randint(0, len(self.bot_names)-1)
            name = self.bot_names[randint]
        return name

    def bot_guess_wins(self, max, last, guess_count):
        if self.hand.got_spades():
            self.guess = max
        else:
            self.guess = 0
        if not last:
            return

        sum_guesses = self.guess + guess_count
        if not sum_guesses == max:
            return
        elif self.guess == 0:
            self.guess = 1
        else:
            self.guess = max - 1
            

    def bot_choose_card(self, suite):
        self.hand.sort()
        self.hand.invert()
        for card in self.hand.cards:
            if card.suite in card.trump_suites:
                return card
            elif card.suite == suite:
                return card
        return self.hand.cards[0]


class Round:
    state_mappings = {
        0: 'Round initializing',
        1: 'Dealing',
        2: 'Guessing number of wins',
        3: 'Player guessing',
        4: 'Playout',
        5: 'Players turn',
        6: 'Next playout',
        -1: 'Round finished'
    }

    def __init__(self, round, round_count, players):
        self.round = round
        self.round_count = round_count
        self.state = self.state_mappings[0]
        self.turn_count = 0
        self.turn_started = False
        self.played_count = 0
        self.round_count = 0
        self.players = players
        self.human_player = self._get_human_player()
        self.done_guessing = []
        self.first_player = None
        self.dealer = None
        self.wins = {player: 0 for player in self.players}
        self.deck = Deck()
        self.dealt = {player: None for player in self.players}
        self.start_index = 0
        self.last_win = None
        self.round_complete = False

    def _get_human_player(self):
        for player in self.players:
            if not player.is_bot:
                return player

    def _set_win(self):
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
        # set round winner for next round
        self.last_win = highest[0]

    def _reset_pile(self):
        self.dealt = {player: None for player in self.players}

    def _reset_guesses(self):
        for player in self.players:
            player.guess = None

    def _check_valid_play(self):
        pass

    def _wrong_input(guesser, max_guess):
        while True:
            try:
                guess = int(input(f'\t{guesser.__str__()}, invalid input. Try again: '))
                if not 1 <= guess <= max_guess:
                    continue
            except (TypeError, ValueError):
                continue
            return guess

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

    def _get_first_player(self):
        if self.last_win:
            return self.players.index(self.last_win)
        guesses = [player.guess for player in self.players]
        return guesses.index(max(guesses))

    def _play_round(self, payload, player):
            try:
                card = int(payload)
                if not 1 <= card <= len(player.hand.cards):
                    return False, 'Invalid inppput, try again'
            except (TypeError, ValueError):
                return False, 'Invalid inppput, try again'
            card -= 1
            self.dealt[player] = player.hand.deal(card)
            for player, card in self.dealt.items():
                if self.players.index(player) == self.start_index:
                    lead_card = card
                    break
            return True, f'Lead card is {lead_card}'

    def _guess_wins(self, guess=None):
        max_guess = self.round
        information = []
        for guesser in self.players:
            if guesser in self.done_guessing:
                continue
            last_guess = True if (guesser is self.players[-1]) else False
            if guesser.is_bot:
                guess_count = sum([(player.guess or 0) for player in self.players])
                guesser.bot_guess_wins(max_guess, last_guess, guess_count)
                information.append(f'{guesser.__str__()} guessed {guesser.guess} wins.')
                self.done_guessing.append(guesser)
            elif self.state == self.state_mappings[3]:
                valid, info = self._validate_player_guess(guesser, guess, last_guess)
                information.append(info)
                if valid:
                    self.done_guessing.append(guesser)
                return valid, information
            if self.state == self.state_mappings[2]:
                if not information:
                    information.append(f'{self.human_player} is the first player to guess')
                return True, information
            else:
                continue
        return True, information

    def _deal(self):
        num_cards = self.round
        information = []
        for recipiant in self.players:
            for _ in range(num_cards):
                recipiant.hand.put(self.deck.deal())
            information.append(f'{num_cards} dealt to {recipiant.__str__()}')
        return information

    def _init_round(self):
        self._reset_guesses()
        self.dealer = self.players[-1]
        information = [f'{self.dealer} is the dealer']
        self.deck.shuffle()
        information.append('Deck shuffled')
        information.append(f'The {self.round} card round is about to start')
        standings = [f'{player.__str__()}: {player.score} points.' for player in self.players]
        information.append(f'The standings are: {" ".join(standings)}')
        return information

    def progress_round(self, payload):
        information = []
        instructions = ''
        if self.state == self.state_mappings[0] or self.state == self.state_mappings[-1]:
            information = self._init_round()
            instructions = 'When ready, press Enter'
            self.state = self.state_mappings[1]
        elif self.state == self.state_mappings[1]:
            information = self._deal()
            information.append(f'{self.players[0]} will start guessing')
            self.state = self.state_mappings[2]
            _, info= self._guess_wins()
            information += info
            instructions = 'Guess how many wins you will have this round:'
            self.state = self.state_mappings[3]
        elif self.state == self.state_mappings[3]:
            valid, information = self._guess_wins(payload)
            if not valid:
                instructions = 'Invalid guess. Try again:'
            elif len(self.done_guessing) == len(self.players):
                self.state = self.state_mappings[4]
                information.append('Guessing is done')
            else:
                _, information = self._guess_wins()
                self.state = self.state_mappings[4]
                information.append('Guessing is done')
        elif self.state == self.state_mappings[5]:
            # 5 := process player input
            valid, info = self._play_round(payload, self.human_player)
            if not valid:
                information = [info] + [f'Your hand: {self.human_player.hand.list_()}']
                instructions = f'Play a card (1 - {len(self.human_player.hand.cards)}):'
                return self.get_state(information, instructions)
            self.state = self.state_mappings[4]
            self.turn_count += 1
        if self.state == self.state_mappings[4]:
            if self.turn_count == 0 and (not self.turn_started):
                self.start_index = self._get_first_player()
                self.first_player = self.players[self.start_index]
                information.append(f'{self.first_player} plays out first')
                instructions = 'Press Enter to start the playout'
                self.turn_started = True
                return self.get_state(information, instructions)
            elif 0 <= self.turn_count < len(self.players):
                player = self.players[(self.start_index + self.turn_count) % len(self.players)]
                if player.is_bot:
                    info = self._bot_play_round(player)
                    information.append(info)
                    instructions = 'Press Enter to progress'
                    self.turn_count += 1
                else:
                    information = [f'Your hand: {player.hand.list_()}']
                    instructions = f'Play a card (1 - {len(player.hand.cards)}):'
                    self.state = self.state_mappings[5]
                    return self.get_state(information, instructions)
            if self.turn_count == len(self.players) and (self.turn_started == True):
                self._set_win()
                information.append('End of this playout')
                instructions = 'Press Enter to progress'
                self.turn_started = False
                self.state = self.state_mappings[6]
        elif self.state == self.state_mappings[6]:
            self.state = self.state_mappings[4]
            self.turn_count = 0
            self.round_count += 1
            self._reset_pile()
            information = ['Pile cleaned']
            if self.round_count == self.round:
                information.append('Setting up next round')
                instructions = 'Press Enter to progress'
                self.state = self.state_mappings[-1]
            else:
                information.append(f'{self.last_win} will start next layout')
                instructions = 'Press Enter to progress'

        return self.get_state(information, instructions)

    def _bot_play_round(self, player):
            player.hand.sort()
            player.hand.invert()
            play_card = None
            if player is self.first_player:
                play_card = 0
            else:
                for player_, card in self.dealt.items():
                    if player_ == self.first_player:
                        lead_card = card
                        break
                for index in range(len(player.hand.cards)):
                    if player.hand.cards[index].suite in Card.trump_suites:
                        play_card = index
                        break
                    elif player.hand.cards[index].suite == lead_card.suite:
                        play_card = index
            if not play_card:
                play_card = 0
            self.dealt[player] = player.hand.deal(play_card)
            return f'{player} played {self.dealt[player]}'

    def _validate_player_guess(self, guesser, guess, last_guess):
        max_guess = self.round
        try:
            guess = int(guess)
            if not 0 <= guess <= max_guess:
                return False, 'Your guess is out of range'
        except (TypeError, ValueError):
            return False, 'Your guess is not valid'
        guesser.guess = guess
        if last_guess:
            sum_guesses = sum([player.guess for player in self.players])
            if sum_guesses == max_guess:
                return False, f'The last guess can\'t be {guess}'
        return True, 'Valid guess'

    def get_state(self, information, instructions):
        wins = [f'{player}: {wins}' for player, wins in self.wins.items()]
        # dealt = [f'{player}: {dealt}' for player, dealt in self.dealt.items()]
        dealt = []
        for player, card in self.dealt.items():
            if self.players.index(player) == self.start_index:
                dealt.append(f'{player}: {card} (LEAD)')
            else:
                dealt.append(f'{player}: {card}')
        guesses = [f'{player}: {player.guess}' for player in self.players]
        state = {
            'state': self.state,
            'player': self.first_player.__str__(),
            'human_player': self.human_player,
            'dealer': self.dealer.__str__(),
            'wins': wins,
            'dealt': dealt,
            'guesses': guesses,
            'last_win': self.last_win,
            'instructions': instructions,
            'information': information
        }
        return state


class Plump:
    """
    state = {
        "round": <Round object>,
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
        self.round = None
        self.players = []
        self.rounds = []
        self.round_count = 0
        self.game_over = False
        self._setup_game(player_list, duration)

    def _setup_game(self, player_list, duration):
        self.rounds = self.round_options[duration]
        for player in player_list:
            while True:
                # make sure names are not duplicated
                new_player = Player(player)
                if new_player.__str__() in [player.__str__() for player in self.players]:
                    continue
                break
            self.players.append(new_player)

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
        self._give_points(result)
        if self.round_count == len(self.rounds) - 1:
            self.game_over = True
            return
        self._arrange_wrt_dealer()
        self.round_count += 1

    def get_state(self):
        score = {player.__str__(): player.score for player in self.players}
        state = {
            "rounds": self.rounds,
            "score": score,
            "round_count": self.round_count+1,
            "game_over": self.game_over,
        }
        return state

    def iterate(self, payload):
        if self.game_over:
            return self.get_state()
        if not self.round:
            self.round = Round(self.rounds[self.round_count], self.round_count, self.players)
        round_updated = self.round.progress_round(payload)
        if round_updated['state'] == self.round.state_mappings[-1]:
            result = self.round.wins
            self.update_state(result)
            self.round = None
        return {
            'game_state': self.get_state(),
            'round_state': round_updated
        }
