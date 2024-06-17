
from model import Plump


if __name__ == '__main__':
    bots = 2
    players = ['Agge'] + [None for _ in range(bots)]
    duration = 3
    game = Plump(players, duration)
    payload = None

    while True:
        new_state = game.iterate(payload)
        print('\n-------------------------------------------------------\n')
        print('game_state:\n', new_state['game_state'])
        print('wins:\n', new_state['round_state']['wins'])
        print('state:\n', new_state['round_state']['state'])
        print('Pile:\n', new_state['round_state']['dealt'])
        print('guesses:\n', new_state['round_state']['guesses'])
        print('Your hand:\n', new_state['round_state']['human_player'].hand.list_())
        print('\n#################### INFORMATION ######################')
        print(new_state['round_state']['information'])
        print('\n#################### INSTRUCTIONS ######################')
        print(new_state['round_state']['instructions'], '\n')
        payload = input('input: ')
        if game.game_over:
            print('\n'*10)
            print('End of game!\n\tFinal state was:')
            print(game.get_state())
            break
