
from model import Plump


players = ['Agge', 'Lise']
duration = 5
# duration = 10
# duration = 15


if __name__ == '__main__':
    kwargs = {'players': players, 'duration': duration}
    game = Plump(**kwargs)
    game.play()
