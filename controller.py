
from model import Plump, Round


players = ['Agge', 'Lise']
duration = 3
# duration = 5
# duration = 10
# duration = 15


if __name__ == '__main__':
    game = Plump()
    game.setup_game(players, duration)
    while True:
        if game.game_over:
            break
        round_count = game.round_count
        round = Round(game.rounds[round_count], round_count, game.players)

        round.init_round()
        round.deal()
        round.guess_wins()
        round.play_round()
        result = round.wins

        game.update_state(result)
        print(game.get_state())

    print('\n'*10)
    print('End of game!\n\tFinal state was:')
    print(game.get_state())