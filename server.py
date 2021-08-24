import random
from pygase import GameState, Backend
from model import Plump, Round

### SETUP ###

# Initialize the game state.
initial_game_state = GameState(
    players={},  # dict with `player_id: player_dict` entries
    turn_id=None,
    game_initialized=False,
    message=None,
    payload=None,
    num_players=2,
)

game = Plump({"duration": 5})

# Define the game loop iteration function.
def time_step(game_state, dt):
    # Before all players join, updating the game state is unnecessary.
    if len(game_state.players.keys()) < game_state.num_players:
        return {}
    
    if not game_state.game_initialized:
        players = [player["name"] for player_id, player in game_state.players.items()]
        game.players.append(players)
        return {"game_initialized": True}

    for round in game.rounds:
        dealer = game.players[-1]
        round = Round(dealer, round, game.rounds, game.players)
        result = round.play()
        game._give_points(result)
        game._arrange_wrt_dealer()
        game.round_count += 1
    print('\n'*10)
    print('End of game!\n\tFinal score was:')
    for player in self.players:
        print(player, player.score)

    playing = game_state.players[game_state.turn_id]

    # for player_id, player in game_state.players.items():
    #     if not player_id == game_state.turn_id:
    #         pass
    #         print(f"{player['name']} has been caught")
    #         return {"turn_id": player_id, "protection": True, "countdown": 5.0}
    return {}


# "MOVE" event handler
def on_move(player_id, new_position, **kwargs):
    return {"players": {player_id: {"position": new_position}}}

# "MESSAGE" event handler
def give_message(message, **kwargs):
    return {"message": message}

# Create the backend.
backend = Backend(initial_game_state, time_step, event_handlers={"MOVE": on_move, "MESSAGE": give_message})

# "JOIN" event handler
def on_join(player_name, game_state, client_address, **kwargs):
    print(f"{player_name} joined.")
    player_id = len(game_state.players)
    # Notify client that the player successfully joined the game.
    backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
    return {
        # Add a new entry to the players dict
        "players": {player_id: {"name": player_name, "points": 0}},
        # If this is the first player to join, make it the chaser.
        "turn_id": player_id if game_state.turn_id is None else game_state.turn_id,
    }


# Register the "JOIN" handler.
backend.game_state_machine.register_event_handler("JOIN", on_join)

### MAIN PROCESS ###

if __name__ == "__main__":
    backend.run(hostname="localhost", port=8080)