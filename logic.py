# CHEGGSS V1.0

# AGENDA - start making legal move checks for each piece,

# At some point need a day to try and clean up comments
# FEN string for tracking not position info? Or custom object?
# Any way to avoid cls.currGame all the time?
# classmethod vs staticmethod
# figure out user_move vs user_input (okay to make prop name variable name?)
# also, user_input should not be prop/variable names in functions that will be used for engine moves
# mapped_move?

# really need to figure out whether to store start/end squares as strings or arrays. Probably arrays. Causing issues in legal move checks.

class Piece():
    empty_square = '-'

    black_king = 'k'
    black_queen = 'q'
    black_rook = 'r'
    black_bishop = 'b'
    black_knight = 'n'
    black_pawn = 'p'

    white_king = 'K'
    white_queen = 'Q'
    white_rook = 'R'
    white_bishop = 'B'
    white_knight = 'N'
    white_pawn = 'P'

    # @classmethod
    # def is_black(cls, piece):
    #     return piece.islower()

    # @classmethod
    # def is_white(cls, piece):
    #     return piece.isupper()
    
    @classmethod
    def color(cls, piece):
        if piece.islower():
            return 'b'
        if piece.isupper():
            return 'w'
        return '-'

class Board():
    # empty_board = [[], [], [], [], [], [], [], []]
    STARTING_BOARD_STATE = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    # starting_game_state = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    # # Will this cause game state to reset everytime Board is instantiated?
    # # Maybe these should be kept in class Game() or something
    # board_state = starting_board_state
    # game_state = starting_game_state

    game_state = {
        "board_state": [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ],
        "to_move": "w",
        "castling_rights": {
            "white": {
                "king_side": True,
                "queen_side": True,
            },
            "black": {
                "king_side": True,
                "queen_side": True,
            }
        },
        "en_passant_target_square": None,
        "halfmove_clock": 0,
        "fullmove_number": 1,
    }


    unicode_dict = {
        'k': '♔',
        'q': '♕',
        'r': '♖',
        'b': '♗',
        'n': '♘',
        'p': '♙',
        'K': '♚',
        'Q': '♛',
        'R': '♜',
        'B': '♝',
        'N': '♞',
        'P': '♟',
        '-': '-'
    }

    # @classmethod
    # def build_position_from_fen(cls, fen_string):
    #     current_position = []
    #     current_rank = []
    #     rank_count = 1
    #     for chr in fen_string:
    #         if rank_count > 8:
    #             return current_position
    #             # More to do
    #         elif chr.isalpha():
    #             current_rank.append(chr)
    #         # (Possibly) don't need to loop for this
    #         elif chr.isnumeric():
    #             for i in range(int(chr)):
    #                 current_rank.append('-')
    #         elif chr == '/':
    #             current_position.append(current_rank)
    #             current_rank = []
    #             rank_count += 1
    #         elif chr == ' ':
    #             if rank_count == 8:
    #                 current_position.append(current_rank)
    #                 current_rank = []
    #                 rank_count += 1
    #                 continue
    #             # More to do
    
    @classmethod
    def render_board(cls, board):
        print("\n")
        board_with_unicode_symbols = [[cls.unicode_dict[cell] for cell in row] for row in board]
        files = 'a b c d e f g h'
        for i, row in enumerate(board_with_unicode_symbols):
            rank = str(8 - i) + ' '
            print(f"{rank} {' '.join(row)}")
        print(f"\n   {files}\n")

class Move():
    # Change end square to target square?
    # takes in square (i.e. "a1") and returns a single number that represents a square.
    # this makes things easier when checking if a move is legal.

    @classmethod
    def map_move_value(cls, user_input):
        start_square, end_square = user_input.split()
        start_square_mapped = 0
        end_square_mapped = 0

        file_map = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
        }

        for chr in start_square:
            if chr.isalpha():
                start_square_mapped += file_map[chr]
            elif chr.isnumeric():
                start_square_mapped += (int(chr) - 1) * 8

        for chr in end_square:
            if chr.isalpha():
                end_square_mapped += file_map[chr]
            elif chr.isnumeric():
                end_square_mapped += (int(chr) - 1) * 8
                
        return [start_square_mapped, end_square_mapped]
    
    @classmethod
    def map_move_coordinates(cls, user_input):
        start_square, end_square = user_input.split()
        start_square_mapped = 0
        end_square_mapped = 0

        file_map = {
            "a": "0",
            "b": "1",
            "c": "2",
            "d": "3",
            "e": "4",
            "f": "5",
            "g": "6",
            "h": "7",
        }

        rank_map = {
            "1": "7",
            "2": "6",
            "3": "5",
            "4": "4",
            "5": "3",
            "6": "2",
            "7": "1",
            "8": "0",
        }

        for chr in start_square:
            if chr.isalpha():
                start_square_mapped = file_map[chr]
            elif chr.isnumeric():
                start_square_mapped = rank_map[chr] + start_square_mapped

        for chr in end_square:
            if chr.isalpha():
                end_square_mapped = file_map[chr]
            elif chr.isnumeric():
                end_square_mapped = rank_map[chr] + end_square_mapped

        return [start_square_mapped, end_square_mapped]

    @classmethod
    def handle_user_move(cls, start_square, end_square):
        pass

    # first check if piece can move like that
    # then make move and check if king is in check
    # will probably need to pass in square values AND string coordinates
    @classmethod
    def is_legal_move(cls, user_input, current_board=None, proposed_board=None):
        # need to prevent same starting and ending square, and squares
        # that don't exist (a0, z6, etc)

        # 8    57 58 59 60 61 62 63 64
        # 7    49 50 51 52 53 54 55 56
        # 6    41 42 43 44 45 46 47 48
        # 5    33 34 35 36 37 38 39 40
        # 4    25 26 27 28 29 30 31 32
        # 3    17 18 19 20 21 22 23 24
        # 2    9  10 11 12 13 14 15 16
        # 1    1  2  3  4  5  6  7  8

        #      a  b  c  d  e  f  g  h
        start_square, end_square = user_input.split()
        return True
    
    @classmethod
    def make_move(cls, move, current_game):
        moving_piece = current_game.game_state["board_state"][int(move[0][0])][int(move[0][1])]
        
        current_game.game_state["board_state"][int(move[1][0])][int(move[1][1])] = moving_piece
        current_game.game_state["board_state"][int(move[0][0])][int(move[0][1])] = Piece.empty_square
        # update game state (whose turn it is, halfmoves, etc.)


    # generate legal moves function 








    # # this is where you left off, you need to make sure active_color is being passed in
    # def legal_rook_move(cls, start_square, end_square, active_color):
    #     # maybe just store array for start and end square rank and file? Separate rank and file variables (4 total)?
    #     # if vs else if?

    #     # check if end_square is in line with start_square horizonally or vertically
    #     if not (start_square[0] == end_square[0]) or (start_square[1] == end_square[1]):
    #         return False
        
    #     end_square_piece = Board.board_state[int(end_square[0])][int(end_square[1])]
    #     # Check that ending square is either unoccupied or occupied by opposite color
    #     if active_color == Piece.color(end_square_piece):
    #         return False
        
    #     # Check that there are no pieces in move path
    #     # Horizontal
    #     if start_square[0] == end_square[0]:
    #         # this messes up if first number in range is bigger than second
    #         # could use step parameter in range, but need to check which is bigger first
    #         for file in range(int(start_square[1]), int(end_square[1])):
    #             if Board.board_state[int(start_square[0])][file] != Piece.empty_square:
    #                 return False
                
    #     # if start_square[1] == end_square[1]:
    #     #     for rank in range(int(start))
