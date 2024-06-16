
from model import Plump, Round


if __name__ == '__main__':
    bots = 2
    players = ['Agge'] + [None for _ in range(bots)]
    duration = 3
    game = Plump(players, duration)

    while True:
        if game.game_over:
            break
        round_count = game.round_count
        round = Round(game.rounds[round_count], round_count, game.players)


        # result = round.play()
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