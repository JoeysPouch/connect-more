from logic.game_screens.menu import run_menu, start_game
from logic.game_screens.game import Game

if __name__ == "__main__":
    run_menu()
    while not start_game():
        print(start_game)
        pass
    Game()
    

