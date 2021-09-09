import random
import time

from pygase import Client



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
