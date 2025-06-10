from logic.game_screens.menu import run_menu, start_game
from logic.game_screens.game import Game, update_globals

if __name__ == "__main__":
    while True:
        run_menu()
        while not start_game():
            pass
        
        update_globals()
        game = Game()
        game.game_loop()
        if not game.return_to_menu:
            break