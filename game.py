from logic import Board, Move
import re

class Game():
    CURRENT_GAME = Board()

    # Does this belong in this class? Helper class?
    @classmethod
    def is_valid_input(cls, user_input):
        pattern = r'^[a-zA-Z][0-9] [a-zA-Z][0-9]$'
        match = re.fullmatch(pattern, user_input)
        return match is not None

    @classmethod
    def prompt_user_move(cls):
        current_position=cls.CURRENT_GAME.game_state["board_state"]
        legal_user_move = None

        if current_position == cls.CURRENT_GAME.STARTING_BOARD_STATE:
            print("\nThank you for challenging Cheggss v1.0 to a game of chess! Your help with testing is appreciated and any feedback is welcome.")
        cls.CURRENT_GAME.render_board(current_position)

        legal_move = False
        while not legal_move:
            user_move = input("Make your move: ")
            if not cls.is_valid_input(user_move):
                print(f"\nMove '{user_move}' is improperly formatted. Moves must be formatted 'start_square end_square'.\nExample: d2 d4\n")
                continue
            if Move.is_legal_move(user_move, cls.CURRENT_GAME):
                legal_user_move = Move.map_move_coordinates(user_move)
                legal_move = True

            else:
                print(f"\n'{user_move}' is not a legal move. Try again.\n")
                continue
        
        Move.make_move(move=legal_user_move, current_game=cls.CURRENT_GAME)
        cls.play_game()

        

    @classmethod
    def engine_move(cls, current_position=CURRENT_GAME.game_state):
        print("Your turn Cheggss! Take your time buddy")
        pass

    # Rename? continue_game?
    @classmethod
    def play_game(cls):
        game_state=cls.CURRENT_GAME.game_state
        # logic for game ending (draw, stalemate, win, loss)
        if game_state["to_move"] == 'w':
            cls.prompt_user_move()
        else:
            cls.engine_move(cls.CURRENT_GAME.game_state)

Game.play_game()
