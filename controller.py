
from model import Plump


players = ['Agge', 'Lise']
num_bots = 2
duration = 5
# duration = 10
# duration = 15


if __name__ == '__main__':
    kwargs = {'players': players, 'duration': duration, 'num_bots': num_bots}
    game = Plump(**kwargs)
    game.play()
